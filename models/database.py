import psycopg2
from PyQt6.QtWidgets import QMessageBox
import logging


class Database:
    def __init__(self):
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def connect(self, dbname, user, password, host):
        try:
            self.logger.info("Попытка подключения к БД")
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host
            )
            self.logger.info("Подключение к БД успешно выполнено")
            return True
        except psycopg2.Error as e:
            QMessageBox.critical(None, "Ошибка подключения", f"Не удалось подключиться к БД:\n{str(e)}")
            self.logger.error(f"Ошибка подключения к БД: {str(e)}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Соединение с БД закрыто")

    def execute_query(self, query, params=None, fetch=False):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
                return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка выполнения запроса: {str(e)}")
            return False
