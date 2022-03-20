import MySQLdb as mysql
from loguru import logger

from db.config import host_name, user_name, password, database_name

def connection_to_database(create_query):
    def wrapper(self, **kwargs):
        try:
            connection = mysql.connect(host=host_name,
                                                user=user_name,
                                                password=password,
                                                database=database_name)
            logger.info(f"Connected to MySQL Server")
            cursor = connection.cursor()
            query = create_query(self, **kwargs)
            logger.info(query)

            if 'INSERT' in query:
                cursor.execute(query)
                connection.commit()
            else:
                cursor.execute(query)
                record = cursor.fetchall()
                return record
        except:
            logger.error("Error while connecting to MySQL")
        finally:
            cursor.close()
            connection.close()
            logger.info("MySQL connection is closed")
    return wrapper

