class NotFound(Exception):
    """
    Исключение, которое представляет ошибку "Страница не найдена" с HTTP-кодом 404.
    """
    code = 404
    txt = 'Страница не найдена'


class NotAllowed(Exception):
    """
    Исключение, которое представляет ошибку "Неподдерживаемый HTTP-метод" с HTTP-кодом 405.
    """
    code = 405
    txt = 'Неподдерживаемый HTTP-метод'