import re
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
    Этот класс представляет серверный объект CCDCServer.
    В данном экземпляре класса могут быть доступны только эти атрибуты,
    если попытаться обратиться к другим атрибутам, то будет выведена ошибка,
    а также это экономит память, т.к. Python не создает словарь для хранения
    атрибутов объекта.
    """
    __slots__ = ('urls', 'settings', 'middlewares')

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleware]]):
        """
        Конструктор класса для инициализации объекта CCDCServer.

        :param urls: Список URL, где каждый элемент списка должен быть типа Url.
        :param settings: Словарь с настройками сервера.
        :param middlewares: Список middleware, являющихся подклассами BaseMiddleware.
        """

        self.urls = urls
        self.settings = settings
        self.middlewares = middlewares

    def __call__(self, environ: dict, start_response):
        """
        Метод __call__ в Python позволяет сделать экземпляр класса "вызываемым" (callable), то есть,
        вы можете вызывать экземпляр этого класса как функцию.

        :param environ: Это словарь, содержащий информацию о текущем запросе.
        :param start_response: Функция обратного вызова для начала ответа сервера.
        :return: Возвращает тело ответа, которое будет передано пользователю.
        """

        EnvironStorage.set_environ(environ)
        EnvironStorage.set_start_response(start_response)
        view = self._get_view(environ)
        request = self._get_request(environ)
        self._apply_middleware_to_request(request)
        response = self._get_response(environ, view, request)
        self._apply_middleware_to_response(response)
        start_response(str(response.status_code), response.headers.items())
        print(environ)

        return iter([response.body])

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
        #  Функция hasattr проверяет, существует ли атрибут с указанным именем (attr)
        #  у объекта (obj)
        if not hasattr(view, method):
            raise NotAllowed

        # Функция getattr возвращает значение атрибута с указанным именем (attr)
        # у объекта (obj)
        return getattr(view, method)(request)

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
