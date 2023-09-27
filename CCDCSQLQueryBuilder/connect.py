import mysql.connector


class DB:
    """
    Класс для подключения к базе данных MySQL.
    """

    def __init__(self, host, user, password, database):
        """
        Конструктор класса DB, инициализирует параметры подключения.

        :param host: Хост базы данных.
        :param user: Пользователь базы данных.
        :param password: Пароль пользователя базы данных.
        :param database: Название базы данных.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.link = None
        self.cursor = None

    def connect(self):
        """
        Метод для установления соединения с базой данных.

        :return: Курсор для выполнения SQL-запросов.
        """
        try:
            self.link = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.link.autocommit = True
            self.cursor = self.link.cursor(dictionary=True)
            return self.cursor
        except mysql.connector.Error as err:
            print(f"Ошибка при подключении к базе данных: {err}")

    def disconnect(self):
        """
        Метод для разрыва соединения с базой данных.
        """
        if self.cursor:
            self.cursor.close()
        if self.link:
            self.link.close()


db = DB(
    host="localhost",
    user="root",
    password="1234",
    database="web_builder"
)

cursor = db.connect()
