from loguru import logger
import psycopg2

from db.config import host_name, user_name, password, database_name

def connection_to_database(create_query):
    def wrapper(self, **kwargs):
        # try:
        connection = psycopg2.connect(
                                    host=host_name,
                                    user=user_name,
                                    password=password,
                                    dbname=database_name
                                    ) 
        logger.info(f"Connected to Server")
        connection.autocommit = True
        with connection.cursor() as cursor:
            query = create_query(self, **kwargs)
            logger.info(query)

            if 'INSERT' in query:
                cursor.execute(query)
                # connection.commit() # autocommit = True
            elif 'CREATE' in query:
                cursor.execute(query)
                logger.info('Creation completed IF NOT EXISTS')
            else:
                cursor.execute(query)
                record = cursor.fetchall()
                return record
        # except:
        #     logger.error("Error while connecting to database")
        # finally:
        #     # cursor.close() # т.к. connection.cursor() через with
        #     connection.close()
        #     logger.info("Connection is closed")
    return wrapper
