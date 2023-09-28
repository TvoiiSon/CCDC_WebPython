class EnvironStorage:
    """

    """
    _environ = None
    _start_response = None

    @classmethod
    def set_environ(cls, environ: dict):
        """

        :param environ:
        :return:
        """
        cls._environ = environ

    @classmethod
    def get_environ(cls):
        """

        :return:
        """
        return cls._environ

    @classmethod
    def set_start_response(cls, start_response):
        """

        :param start_response:
        :return:
        """
        cls._start_response = start_response

    @classmethod
    def get_start_response(cls):
        """

        :return:
        """
        return cls._start_response
