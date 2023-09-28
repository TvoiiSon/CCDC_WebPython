class InsertQuery:
    """
    Класс для создания SQL-запросов INSERT.
    """
    __slots__ = {"table_name", "data"}

    def __init__(self, table_name: str, data: dict):
        """
        Инициализирует объект InsertQuery.

        :param table_name: Имя таблицы, в которую будет выполняться вставка данных.
        :param data: Словарь с данными для вставки в виде {имя_колонки: значение}.
        """
        if not table_name:
            raise ValueError("Имя таблицы обязательно")

        self.table_name = table_name
        self.data = data

    def build_query(self):
        """
        Создает SQL-запрос INSERT на основе заданных параметров.

        :return: Кортеж, содержащий строку SQL-запроса и список параметров для безопасной вставки значений.
        """
        if not self.data:
            raise ValueError("Нет данных для вставки")

        columns = ", ".join(self.data.keys())
        values = ", ".join(["%s" for _ in self.data.values()])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
        query_params = list(self.data.values())
        return query, query_params
