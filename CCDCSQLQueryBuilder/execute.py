from CCDCSQLQueryBuilder.connect import DB
import mysql.connector


async def execute_query(query: str, params=None, *args):
    """
    Выполняет SQL-запрос с использованием заданного курсора и выполняет дополнительные действия,
    определенные в *args и **kwargs.

    :param query: Строка SQL-запроса для выполнения.
    :param params: Параметры, передаваемые в SQL-запрос (опционально).
    :param args: Дополнительные позиционные аргументы.
    """

    db = DB(
        host="localhost",
        user="root",
        password="1234",
        database="builder"
    )

    cursor = db.connect()

    result = None

    try:
        with cursor as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)

            for arg in args:
                if arg == 'fetchone':
                    result = cur.fetchone()
                elif arg == 'fetchall':
                    result = cur.fetchall()

    except mysql.connector.Error as err:
        print(f"Ошибка при выполнении запроса: {err}")

    db.disconnect()

    return result
