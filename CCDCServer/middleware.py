from CCDCServer.request import Request
from CCDCServer.response import Response
from uuid import uuid4
from urllib.parse import parse_qs


class BaseMiddleware:
    """
    Базовый класс для всех промежуточных слоев. Он определяет два метода: to_request и to_response,
    которые пока не выполняют никаких действий. Промежуточные слои будут наследоваться от этого базового
    класса и переопределять эти методы для выполнения своей функциональности.
    """

    def to_request(self, request: Request):
        """
        Этот метод может быть переопределен в производных классах для выполнения действий
        над объектом запроса перед обработкой.

        :param request: Объект запроса (Request)
        """

        pass

    def to_response(self, response: Response):
        """
        Этот метод может быть переопределен в производных классах для выполнения действий
        над объектом ответа перед отправкой клиенту.

        :param response: Объект ответа (Response)
        """

        pass


class Session(BaseMiddleware):
    """
    Конкретный промежуточный слой для работы с сессиями. Он наследует функциональность из BaseMiddleware
    и переопределяет методы to_request и to_response.
    """

    def to_request(self, request: Request):
        """
        Этот метод проверяет наличие куки с именем 'session_id' в HTTP-запросе. Если куки существует,
        то извлекает значение 'session_id' и сохраняет его в атрибут extra объекта request.

        :param request: Объект запроса (Request)
        """

        cookie = request.environ.get('HTTP_COOKIE', None)
        if not cookie:
            return
        session_id = parse_qs(cookie)['session_id'][0]
        request.extra['session_id'] = session_id

    def to_response(self, response: Response):
        """
        Этот метод проверяет, существует ли атрибут 'session_id' в объекте request. Если атрибут отсутствует,
        то генерирует новый уникальный 'session_id' с помощью uuid4() и устанавливает его как куки в заголовке
        ответа 'Set-Cookie'.

        :param response: Объект ответа (Response)
        """

        if not response.request.extra.get('session_id'):
            response.update_headers(
                {'Set-Cookie': f'session_id={uuid4()}'}
            )


# Список middlewares, который включает в себя только один промежуточный слой - Session.
# Этот список будет использоваться в вашем Веб-Фреймворке для применения промежуточных слоев к запросам и ответам.
middlewares = [
    Session
]
