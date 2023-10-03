import re
import hashlib
import tracemalloc
from datetime import datetime, timedelta
from typing import List, Type
from CCDCServer.urls import Url
from CCDCServer.exceptions import NotFound, NotAllowed
from CCDCServer.view import View
from CCDCServer.request import Request
from CCDCServer.response import Response
from CCDCServer.middleware import BaseMiddleware
from CCDCServer.storage_environ import EnvironStorage


class CCDCServer:
    """
    Этот класс представляет объект CCDCServer.
    В экземпляре этого класса доступны только следующие атрибуты.
    Попытка доступа к другим атрибутам вызовет ошибку.
    Это также экономит память, так как Python не создает словарь
    для хранения атрибутов объекта.
    """
    __slots__ = ('urls', 'settings', 'middlewares')

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleware]]):
        """
        Конструктор для инициализации объекта CCDCServer.

        :param urls: Список URL, где каждый элемент должен быть типа Url.
        :param settings: Словарь с настройками сервера.
        :param middlewares: Список middleware, являющихся подклассами BaseMiddleware.
        """
        self.urls = urls
        self.settings = settings
        self.middlewares = middlewares

        tracemalloc.start()

    def __call__(self, environ: dict, start_response):
        """
        Метод __call__ в Python позволяет сделать экземпляр класса "вызываемым", что означает,
        что вы можете вызывать экземпляр этого класса как функцию.

        :param environ: Это словарь, содержащий информацию о текущем запросе.
        :param start_response: Функция обратного вызова для начала ответа сервера.
        :return: Возвращает тело ответа для передачи пользователю.
        """
        try:
            EnvironStorage.set_environ(environ)
            EnvironStorage.set_start_response(start_response)
            view = self._get_view(environ)
            request = self._get_request(environ)
            self._apply_middleware_to_request(request)
            response = self._get_response(environ, view, request)
        except NotFound:
            response = self._handle_404()
        except NotAllowed:
            response = self._handle_405()

        start_response(str(response.status_code), response.headers.items())
        return iter([response.body])

    def __del__(self):
        tracemalloc.stop()

    @staticmethod
    def _prepare_url(url: str):
        """
        Приватный метод, который удаляет завершающий слэш из URL, если он есть.

        :param url: Входной URL.
        :return: Возвращает чистый URL.
        """
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        """
        Метод ищет соответствующий view (класс, обрабатывающий запрос) для переданного URL.

        :param raw_url: Начальный (сырой) URL.
        :return: Возвращает либо 404 (NotFound), либо путь до страницы (View).
        """
        url = self._prepare_url(raw_url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        raise NotFound

    def _get_view(self, environ: dict) -> View:
        """
        Метод получает view для текущего запроса, используя environ['PATH_INFO'] для определения URL.

        :param environ: Это словарь, содержащий информацию о текущем запросе.
        :return: Возвращает объект View, который будет обрабатывать запрос.
        """
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)()
        return view

    def _get_request(self, environ: dict):
        """
        Метод создает объект запроса (Request) на основе данных из environ и настроек (settings).

        :param environ: Это словарь, содержащий информацию о текущем запросе.
        :return: Возвращает объект запроса (Request).
        """
        return Request(environ, self.settings)

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request) -> Response:
        """
        Метод определяет HTTP-метод текущего запроса (environ['REQUEST_METHOD']), а затем
        вызывает соответствующий метод в объекте view. Если метод не существует, вызывается исключение NotAllowed.

        :param environ: Это словарь, содержащий информацию о текущем запросе.
        :param view: Объект View, который обрабатывает запрос.
        :param request: Объект запроса (Request).
        :return: Объект ответа (Response).
        """
        method = environ['REQUEST_METHOD'].lower()
        if not hasattr(view, method):
            raise NotAllowed

        response = getattr(view, method)(request)

        if response.status_code == 200:
            response_body = response.body

            etag = hashlib.sha256(response_body).hexdigest()
            response.headers['ETag'] = f'"{etag}"'
            response.headers['Cache-Control'] = 'max-age=3600'  # Например, кэшировать на 1 час
            response.headers['Expires'] = (datetime.now() + timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
            response.headers['Last-Modified'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

            if 'HTTP_IF_NONE_MATCH' in environ and 'HTTP_IF_MODIFIED_SINCE' in environ:
                client_etag = environ['HTTP_IF_NONE_MATCH']
                client_modified = datetime.strptime(environ['HTTP_IF_MODIFIED_SINCE'], '%a, %d %b %Y %H:%M:%S GMT')

                if etag == client_etag and datetime.now() - client_modified < timedelta(hours=1):
                    response.status_code = 304
                    response.body = b''
                    response.headers.pop('Cache-Control', None)
                    response.headers.pop('Expires', None)

        return response

    def _apply_middleware_to_request(self, request: Request):
        """
        Метод применяет middleware к объекту запроса. Он проходит по списку middleware
        и вызывает метод to_request для каждого из них.

        :param request: Объект запроса (Request).
        :return: Ничего не возвращает.
        """
        for i in self.middlewares:
            i().to_request(request)

    def _apply_middleware_to_response(self, response: Response):
        """
        Метод применяет middleware к объекту ответа. Он проходит по списку middleware
        и вызывает метод to_response для каждого из них.

        :param response: Объект ответа (Response).
        :return: Ничего не возвращает.
        """
        for i in self.middlewares:
            i().to_response(response)

    @staticmethod
    def _handle_404(request: Request = None) -> Response:
        """
        Метод для обработки страницы 404 (Not Found).

        :param request: Объект запроса (Request).
        :return: Объект Response для страницы 404.
        """
        response = Response(request, status_code=404, body="404 - Страница не найдена")
        return response

    @staticmethod
    def _handle_405(request: Request = None) -> Response:
        """
        Метод для обработки страницы 405 (Метод не разрешен).

        :param request: Объект запроса (Request).
        :return: Объект Response для страницы 405.
        """
        response = Response(request, status_code=405, body="405 - Метод не разрешен")
        return response
