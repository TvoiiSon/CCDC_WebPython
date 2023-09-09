from CCDCServer.view import View
from CCDCServer.exceptions import NotFound, NotAllowed
from CCDCServer.urls import Url
from CCDCServer.request import Request
from CCDCServer.response import Response
from typing import Type, List
from pprint import pprint
import re


class Redirect:
    __slots__ = ('urls', 'url', 'settings')

    def __init__(self, urls: List[Url], url: str, settings: dict):
        self.urls = urls
        self.url = url
        self.settings = settings
        print(self.url)

    def invoke(self, environ: dict, start_response):
        pprint(environ)
        view = self._get_view(environ)
        request = self._get_request(environ)
        response = self._get_response(environ, view, request)
        start_response(str(response.status_code), response.headers.items())

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
        view = self._find_view(self.url)()
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
