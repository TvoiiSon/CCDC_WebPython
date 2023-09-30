class EnvironStorage:
    """
    Класс для хранения данных окружения и функции start_response в контексте текущего запроса.
    """

    _environ = None
    _start_response = None

    @classmethod
    def set_environ(cls, environ: dict):
        """
        Устанавливает словарь окружения (environ) текущего запроса.

        :param environ: Словарь с информацией о текущем запросе.
        :return: Ничего не возвращает.
        """
        cls._environ = environ

    @classmethod
    def get_environ(cls):
        """
        Получает словарь окружения (environ) текущего запроса.

        :return: Словарь с информацией о текущем запросе.
        """
        return cls._environ

    @classmethod
    def set_start_response(cls, start_response):
        """
        Устанавливает функцию start_response текущего запроса.

        :param start_response: Функция обратного вызова для начала ответа сервера.
        :return: Ничего не возвращает.
        """
        cls._start_response = start_response

    @classmethod
    def get_start_response(cls):
        """
        Получает функцию start_response текущего запроса.

        :return: Функция обратного вызова для начала ответа сервера.
        """
        return cls._start_response
