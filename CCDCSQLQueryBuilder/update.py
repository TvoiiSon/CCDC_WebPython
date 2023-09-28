class UpdateQuery:
    """
    Класс для создания SQL-запроса UPDATE.
    """

    def __init__(self, table_name, data, **kwargs):
        """
        Инициализирует объект UpdateQuery.

        :param table_name: Имя таблицы, которую необходимо обновить.
        :param data: Словарь, содержащий пары ключ-значение для обновления в таблице.
        :param kwargs: Дополнительные аргументы (например, conditions для фильтрации).
        """

        if not table_name:
            raise ValueError("Имя таблицы обязательно")

        self.table_name = table_name
        self.data = data
        self.conditions = kwargs.get("conditions", [])

    def build_query(self):
        """
        Создает SQL-запрос UPDATE на основе данных объекта.

        :return: Строка с SQL-запросом UPDATE.
        """

        update_pairs = [f"{key} = '{value}'" for key, value in self.data.items()]
        update_str = ", ".join(update_pairs)
        conditions_str = " AND ".join(self.conditions) if self.conditions else ""

        query = f"UPDATE {self.table_name} SET {update_str}"
        if conditions_str:
            query += f" WHERE {conditions_str}"

        return query
