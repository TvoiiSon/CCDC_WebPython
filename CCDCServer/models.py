from CCDCSQLQueryBuilder.select import SelectQuery
from CCDCSQLQueryBuilder.insert import InsertQuery
from CCDCSQLQueryBuilder.execute import execute_query


class Authentication:
    """
    Класс для аутентификации пользователей.
    """
    __slots__ = {"login", "password"}

    def __init__(self, login: str, password: str):
        """
        Инициализирует объект Authentication.

        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        """

        if not login:
            raise ValueError("Не передан параметр login")
        elif not password:
            raise ValueError("Не передан параметр password")
        self.login = login
        self.password = password

    def _select_user(self):
        """
        Выполняет запрос к базе данных для выбора пользователя по логину и паролю.

        :return: Результат запроса к базе данных (одна запись) или None, если пользователь не найден.
        """

        select_user = SelectQuery("users", "login", "password")
        select_user.conditions.append("login = %s")
        select_user.conditions.append("password = %s")
        select_user.params.append(self.login)
        select_user.params.append(self.password)
        query, params = select_user.build_query()
        return execute_query(query, params, "fetchone")

    def _create_user(self):
        """
        Создает новую запись пользователя в базе данных.

        :return: Ничего не возвращает.
        """

        data_to_insert = {"login": f"{self.login}", "password": f"{self.password}"}
        insert_query = InsertQuery("users", data_to_insert)
        query, params = insert_query.build_query()
        execute_query(query, params)

    def auth(self):
        """
        Выполняет аутентификацию пользователя.

        :return: True, если аутентификация успешна, иначе False.
        """

        res = self._select_user()
        if res is not None:
            return True
        else:
            return False

    def reg(self):
        """
        Регистрирует нового пользователя.

        :return: True, если регистрация успешна (новый пользователь добавлен), иначе False (пользователь уже существует).
        """

        res = self._select_user()
        if res is not None:
            return False
        else:
            self._create_user()
            return True
