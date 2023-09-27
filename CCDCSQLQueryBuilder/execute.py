from CCDCSQLQueryBuilder.connect import cursor
import mysql.connector


def execute_query(query, params=None):
    """
    Выполняет SQL-запрос с использованием заданного курсора.

    :param query: Строка SQL-запроса для выполнения.
    :param params: Параметры, передаваемые в SQL-запрос (опционально).
    """
    try:
        with cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
    except mysql.connector.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")
