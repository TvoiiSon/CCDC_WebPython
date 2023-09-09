from urllib.parse import parse_qs


class Request:
    """
    Класс Request предназначен для представления HTTP-запроса в веб-фреймворке и предоставляет методы для доступа
    к параметрам GET и POST, а также к другой информации о запросе и настройкам.
    """

    def __init__(self, environ: dict, settings: dict):
        """
        Конструктор класса Request, принимающий два аргумента.

        :param environ: Словарь, содержащий информацию о текущем запросе
        :param settings: Словарь с настройками сервера
        """

        # Создание словаря GET, который будет содержать параметры GET-запроса
        self.build_get_params_dict(environ['QUERY_STRING'])

        # Создание словаря POST, который будет содержать параметры POST-запроса
        self.build_post_params_dict(environ['wsgi.input'].read())

        # Сохранение словаря environ, содержащего информацию о запросе
        self.environ = environ

        # Сохранение словаря с настройками
        self.settings = settings

        # Создание пустого словаря extra, который может использоваться для дополнительных данных
        self.extra = {}

    def __getattr__(self, item):
        """
        Этот метод позволяет получать атрибуты объекта Request с помощью точечной нотации.

        :param item: Имя атрибута
        :return: Значение атрибута из словаря extra
        """

        return self.extra.get(item)

    def build_get_params_dict(self, raw_params: str):
        """
        Этот метод разбирает строку запроса raw_params и создает словарь GET,
        который содержит параметры GET-запроса в виде пар ключ-значение.

        :param raw_params: Строка запроса
        :return: Ничего не возвращает
        """

        self.GET = parse_qs(raw_params)

    def build_post_params_dict(self, raw_bytes: bytes):
        """
        Этот метод принимает байтовые данные raw_bytes, которые предположительно содержат параметры POST-запроса.
        Он декодирует байты, предполагая, что они в кодировке UTF-8, и создает словарь POST,
        который содержит параметры POST-запроса в виде пар ключ-значение.

        :param raw_bytes: Байтовые данные, которые предположительно содержат параметры POST-запроса
        :return: Ничего не возвращает
        """

        raw_params = raw_bytes.decode("utf-8")
        self.POST = parse_qs(raw_params)
