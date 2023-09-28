class SelectQuery:
    """
    Класс для создания SQL-запросов SELECT.
    """

    def __init__(self, table_name, *args, **kwargs):
        """
        Инициализирует объект SelectQuery.

        :param table_name: Имя таблицы, из которой будет выбираться данные (обязательный параметр).
        :param args: Список колонок, которые следует выбрать (опциональный).
        :param kwargs: Дополнительные аргументы:
            - conditions: Список условий для фильтрации результатов (опциональный).
            - order_by: Название колонки для сортировки результатов (опциональный).
            - like_column: Название колонки для операции LIKE (опциональный).
            - like_value: Значение для операции LIKE (опциональный).
        """
        if not table_name:
            raise ValueError("Имя таблицы обязательно")

        self.table_name = table_name
        self.columns = args
        self.conditions = kwargs.get("conditions", [])
        self.order_by = kwargs.get("order_by", None)
        self.like_column = kwargs.get("like_column", None)
        self.like_value = kwargs.get("like_value", None)
        self.params = []

    def build_query(self):
        """
        Создает SQL-запрос SELECT на основе заданных параметров.

        :return: Кортеж, содержащий строку SQL-запроса и список параметров для безопасной вставки значений.
        """
        columns_str = ", ".join(self.columns) if self.columns else "*"
        conditions_str = " AND ".join(self.conditions) if self.conditions else ""
        order_by_str = f" ORDER BY {self.order_by}" if self.order_by else ""
        like_str = ""

        query_params = self.params

        if self.like_column and self.like_value:
            like_str = f" AND {self.like_column} LIKE %s"
            query_params.append(f'%{self.like_value}%')

        query = f"SELECT {columns_str} FROM {self.table_name}"
        if conditions_str:
            query += f" WHERE {conditions_str}"
        query += like_str
        query += order_by_str

        return query, query_params
