from pprint import pprint


class EnvironStorage:
    _environ = None
    _start_response = None

    @classmethod
    def set_environ(cls, environ: dict):
        cls._environ = environ

    @classmethod
    def get_environ(cls):
        return cls._environ

    @classmethod
    def set_start_response(cls, start_response):
        cls._start_response = start_response

    @classmethod
    def get_start_response(cls):
        return cls._start_response
