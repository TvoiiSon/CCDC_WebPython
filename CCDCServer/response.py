from CCDCServer.request import Request


class Response:
    def __init__(self, request: Request, status_code: int = 200, headers: dict = None, body: str = ''):
        """
        Конструктор класса Response.

        :param request: Объект класса Request, связанный с данным HTTP-ответом
        :param status_code: Целочисленный HTTP-статус-код ответа (по умолчанию 200 - "OK")
        :param headers: Словарь с HTTP-заголовками ответа (по умолчанию пустой словарь)
        :param body: Строка, содержащая тело ответа (по умолчанию пустая строка)
        """

        self.status_code = status_code
        self.headers = {}
        self.body = b''
        self._set_base_headers()
        if headers is not None:
            self.update_headers(headers)
        self._set_body(body)
        self.request = request
        self.extra = {}

    def __getattr__(self, item):
        """
        Этот метод позволяет получать атрибуты объекта Response с помощью точечной нотации.

        :param item: Имя атрибута
        :return: Значение атрибута из словаря extra
        """

        return self.extra.get(item)

    def _set_base_headers(self):
        """
        Этот метод устанавливает базовые HTTP-заголовки ответа, такие как Content-Type и Content-Length.

        :return: Ничего не возвращает
        """

        self.headers = {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Length': 0
        }

    def _set_body(self, raw_body: str):
        """
        Этот метод устанавливает тело ответа, преобразуя строку raw_body в байтовый формат, используя кодировку UTF-8.
        Затем обновляется заголовок Content-Length, чтобы он соответствовал длине тела ответа.

        :param raw_body: Строка, устанавливающая тело ответа
        :return: Ничего не возвращает
        """

        self.body = raw_body.encode('utf-8')
        self.update_headers(
            {'Content-Length': str(len(self.body))}
        )

    def update_headers(self, headers: dict):
        """
        Этот метод позволяет обновлять заголовки ответа, добавляя или изменяя HTTP-заголовки на основе словаря
        headers, переданного в качестве аргумента.

        :param headers: Словарь с заголовками ответа
        :return: Ничего не возвращает
        """

        self.headers.update(headers)
