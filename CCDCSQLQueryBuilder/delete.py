class DeleteQuery:
    """
    Класс для создания SQL-запросов DELETE.
    """

    def __init__(self, table_name: str, **kwargs):
        """
        Инициализирует объект DeleteQuery.

        :param table_name: Имя таблицы, из которой будет выполняться удаление.
        :param kwargs: Дополнительные аргументы.
          - conditions: Список условий для фильтрации строк перед удалением.
        """

        if not table_name:
            raise ValueError("Имя таблицы обязательно")

        self.table_name = table_name
        self.conditions = kwargs.get("conditions", [])

    def build_query(self):
        """
        Создает SQL-запрос DELETE на основе заданных параметров.

        :return: Строка SQL-запроса DELETE.
        """

        conditions_str = " AND ".join(self.conditions) if self.conditions else ""

        query = f"DELETE FROM {self.table_name}"
        if conditions_str:
            query += f" WHERE {conditions_str}"

        return query
