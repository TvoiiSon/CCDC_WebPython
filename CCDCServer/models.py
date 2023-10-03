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

    async def _select_user(self):
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
        return await execute_query(query, params, "fetchone")

    async def _create_user(self):
        """
        Создает новую запись пользователя в базе данных.

        :return: Ничего не возвращает.
        """

        data_to_insert = {"hash": f"{self.login}", "password": f"{self.password}"}
        insert_query = InsertQuery("users", data_to_insert)
        query, params = insert_query.build_query()
        await execute_query(query, params)

    async def _insert_hash(self):
        user = self._select_user()
        if not user:
            return False
        data_to_insert = {"hash": f"{self.login}", "password": f"{self.password}"}

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

        :return: True, если регистрация успешна (новый пользователь добавлен), иначе False (пользователь уже существует)
        """

        res = self._select_user()
        if res is not None:
            return False
        else:
            self._create_user()
            return True


class ManagingProject:
    def __init__(self, username: str):
        if not username:
            raise ValueError("Не передан параметр username")
        self.username = username

    def create_project(self):
        pass

    def delete_project(self):
        pass

    def copy_project(self):
        pass


class ManagingPages:
    def __init__(self, site_name: str):
        if not site_name:
            raise ValueError("Не передан параметр username")
        self.site_name = site_name

    def create_page(self):
        pass

    def copy_page(self):
        pass

    def delete_page(self):
        pass

    def settings_page(self):
        pass


class ManagingBlocks:
    def __init__(self):
        pass

    def create_block(self):
        pass

    def append_block(self):
        pass

    def delete_block(self):
        pass

    def copy_block(self):
        pass

    def setting_block(self):
        pass
