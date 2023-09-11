from CCDCServer.request import Request
from CCDCServer.response import Response


class Redirect(Response):
    """
    Класс, представляющий ответ, который должен выполнить переадресацию.

    :attr status_code (int): Код состояния для переадресации (302 - Found).
    :attr headers (dict): Заголовки ответа, включая "Location" для указания целевого URL.

    :arg request (Request): Объект запроса (Request), который будет использоваться в ответе.
    :arg location (str): URL, на который нужно выполнить переадресацию.
    """

    __slots__ = ("status_code", "headers")

    def __init__(self, request: Request, location: str):
        """
        Инициализация объекта RedirectResponse.

        :param request (Request): Объект запроса (Request), который будет использоваться в ответе.:
        :param location (str): URL, на который нужно выполнить переадресацию.
        """

        super().__init__(request)
        self.status_code = 302  # Код состояния для переадресации (Found)
        self.headers['Location'] = location
