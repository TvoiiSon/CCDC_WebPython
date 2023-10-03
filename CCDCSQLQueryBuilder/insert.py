class InsertQuery:
    """
    Класс для создания SQL-запросов INSERT.
    """
    __slots__ = {"table_name", "data", "conditions"}

    def __init__(self, table_name: str, data: dict, conditions: dict = None):
        """
        Инициализирует объект InsertQuery.

        :param table_name: Имя таблицы, в которую будет выполняться вставка данных.
        :param data: Словарь с данными для вставки в виде {имя_колонки: значение}.
        :param conditions: Словарь с данными для выполнения условия вставки.
        """

        if not table_name:
            raise ValueError("Имя таблицы обязательно")

        self.table_name = table_name
        self.data = data
        self.conditions = conditions or {}

    def build_query(self):
        """
        Создает SQL-запрос INSERT на основе заданных параметров.

        :return: Кортеж, содержащий строку SQL-запроса и список параметров для безопасной вставки значений.
        """
        if not self.data:
            raise ValueError("Нет данных для вставки")
        columns = ", ".join(self.data.keys())
        values = ", ".join(["%s" for _ in self.data.values()])
        conditions = " AND ".join([f"{column} = %s" for column in self.conditions.keys()])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
        if conditions:
            query += f" WHERE {conditions}"
        query_params = list(self.data.values()) + list(self.conditions.values())
        return query, query_params
