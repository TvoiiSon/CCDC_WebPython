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

    def __init__(self, cookie_name='session_id', cookie_value=None):
        """
        Инициализирует объект Session с именем куки и его начальным значением.

        :param cookie_name: Имя куки (по умолчанию 'session_id')
        :param cookie_value: Начальное значение куки (по умолчанию None)
        """

        self.cookie_name = cookie_name
        self.cookie_value = cookie_value or str(uuid4())

    def to_request(self, request: Request):
        """
        Этот метод проверяет наличие куки с заданным именем в HTTP-запросе. Если куки существует,
        то извлекает его значение и сохраняет его в атрибут extra объекта request.

        :param request: Объект запроса (Request)
        """

        cookie = request.environ.get('HTTP_COOKIE', None)
        if cookie:
            cookies = parse_qs(cookie)
            if self.cookie_name in cookies:
                request.extra[self.cookie_name] = cookies[self.cookie_name][0]

    def to_response(self, response: Response):
        """
        Этот метод проверяет, существует ли атрибут с именем куки в объекте request. Если атрибут отсутствует,
        то устанавливает куки с заданным именем и значением в заголовке ответа 'Set-Cookie'.

        :param response: Объект ответа (Response)
        """

        if not response.request.extra.get(self.cookie_name):
            max_age = 2_700_000  # примерно месяц
            response.update_headers(
                {'Set-Cookie': f'{self.cookie_name}={self.cookie_value}; Max-Age={max_age}'}
            )


middlewares = [
    Session
]
