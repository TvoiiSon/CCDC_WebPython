class Session:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    def set_cookie(self, key, value, expires=None, path='/', domain=None, secure=False, http_only=False):
        """
        Устанавливает куки в ответе.

        :param key: Имя куки.
        :param value: Значение куки.
        :param expires: Дата истечения срока действия куки (datetime).
        :param path: Путь, для которого куки действительны.
        :param domain: Домен, для которого куки действительны.
        :param secure: Установите True, если куки должны передаваться только по HTTPS.
        :param http_only: Установите True, если куки должны быть доступны только через HTTP (не JavaScript).
        """

        # Создаем строку куки
        cookie = f"{key}={value}"

        # Добавляем опциональные атрибуты
        if expires:
            cookie += f"; expires={expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}"
        if path:
            cookie += f"; path={path}"
        if domain:
            cookie += f"; domain={domain}"
        if secure:
            cookie += "; secure"
        if http_only:
            cookie += "; HttpOnly"

        # Добавляем куки в заголовки ответа
        self.response.headers['Set-Cookie'] = cookie

    def delete_cookie(self, key):
        """
        Удаляет куки из ответа.

        :param key: Имя куки для удаления.
        """

        # Устанавливаем куки с истекшим сроком действия
        expires = "Thu, 01 Jan 1970 00:00:00 GMT"
        cookie = f"{key}=; expires={expires}; path=/"

        # Добавляем куки в заголовки ответа
        self.response.headers['Set-Cookie'] = cookie

    def get_cookie(self, key):
        """
        Получает значение куки из запроса.

        :param key: Имя куки, значение которого нужно получить.
        :return: Значение куки, если оно присутствует в запросе, иначе None.
        """

        # Извлекаем значение куки с заданным именем из запроса
        return self.request.cookies.get(key)
