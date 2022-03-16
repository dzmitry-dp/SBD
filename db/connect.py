import mysql.connector as sql
from mysql.connector import Error
from loguru import logger

from db.config import root_password, database_name

def connection_to_database(query_func):
    def wrapper(self, **kwargs):
        try:
            connection = sql.connect(host='localhost',
                                                user='root',
                                                password=root_password,
                                                database=database_name)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                logger.info(f"Connected to MySQL Server version {db_Info}")
                cursor = connection.cursor()
                logger.info(query_func(self, **kwargs))
                if kwargs.get('data', None) != None:
                    cursor.execute(query_func(self, **kwargs))
                    connection.commit()
                else:
                    cursor.execute(query_func(self, **kwargs))

                if "SELECT" in query_func(self, **kwargs):
                    record = cursor.fetchall()
                    logger.info(f"Select to database: {record}")
                    return record

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    return wrapper

