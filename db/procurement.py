from loguru import logger
import pandas as pd
import sqlalchemy

import db.config as db_config
from db.connect import connection_to_database

table = {
        'table_name': 'test',
        'col_ty': {
            'Id': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
            'Date': 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP',
            'Name': 'VARCHAR(255)',
            'Price_ZL': 'FLOAT',
            'Price_EUR': 'FLOAT',
            'Link': 'TEXT', 
            'Department': 'VARCHAR(255)', 
            'Project': 'VARCHAR(255)',
            'Comments': 'VARCHAR(255)',
        }
    }

example_values = {
        'Date': "'2022-03-03'",
        'Name': "'Трубка шланга для пылесоса с метражом 20мм длина 50 м'",
        'Price_ZL': '84.04',
        'Price_EUR': '64.33',
        'Link': "'https://allegro.pl/moje-allegro/zakupy/kupione/ddb72880-9b06-11ec-a466-1d12e6b7c649'", 
        'Department': "'Столярка'", 
        'Project': "'Reactor - Prague'",
        'Comments': "'Не выставляют фактуру'",
    }


class ProcurementDataBaseQuery:
    def __init__(self):
        logger.info(f'class {self.__class__.__name__}')
        self.query = ''

    @connection_to_database
    def create_database(self, database_name=db_config.database_name):
        return f"CREATE DATABASE {database_name};"

    @connection_to_database
    def create_table(self, data: dict = table):
        table_name: str = data['table_name']
        columns_and_types: dict = data['col_ty']

        for column in columns_and_types.keys():
            self.query += f"{column} {columns_and_types[column]}, "

        return f"CREATE TABLE IF NOT EXISTS {table_name} ({self.query[:-2]});"

    @connection_to_database
    def write_values_to_the_table(self, data=None, table_name: str = db_config.table_name):
        table_name: str = table_name

        if data == None:
            columns_and_values: dict = example_values
        else:
            columns_and_values: dict = data

        columns = list(columns_and_values.keys())
        values = list(columns_and_values.values())
        return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"

    @connection_to_database
    def show_all_columns_from_table(self, table_name=db_config.table_name):
        columns = ', '.join(list(table['col_ty'].keys()))
        return f"SELECT {columns} FROM {table_name};"

    @connection_to_database
    def del_table(self, table_name=db_config.table_name):
        return f"DROP TABLE {table_name};"

    @connection_to_database
    def del_database(self, database_name=db_config.database_name):
        return f"DROP DATABASE {database_name};"

    @connection_to_database
    def show_tables_on_database(self):
        return "SHOW TABLES;"

    @connection_to_database
    def show_databases_in_mysql(self):
        return "SHOW DATABASES;"


class MySQLwithPandas:
    def import_excel_file_to_mysql_database(self, database_name=db_config.database_name, table_name=db_config.table_name):
        "Если загружаем из excel то убираем индексы которые в таблице excel"
        df: pd.DataFrame = pd.read_excel('./static/procurement.xlsx', engine='openpyxl')

        sql_engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{db_config.password}@127.0.0.1/{database_name}', pool_recycle=3600)
        db_connection = sql_engine.connect()

        dtype = {
            'Date': sqlalchemy.types.DATETIME(),
            'Name': sqlalchemy.types.VARCHAR(length=255),
            'Price_ZL': sqlalchemy.types.FLOAT(),
            'Price_EUR': sqlalchemy.types.FLOAT(),
            'Link': sqlalchemy.types.TEXT(), 
            'Department': sqlalchemy.types.VARCHAR(length=255), 
            'Project': sqlalchemy.types.VARCHAR(length=255),
            'Comments': sqlalchemy.types.TEXT(),
        }

        try:
            frame = df.to_sql(name=table_name, con=db_connection, if_exists='append', index=False, method='multi', dtype=dtype);
        except sqlalchemy.exc.DataError:
            print('Error')
        else:
            print("Successfully.")
        finally:
            db_connection.close()

    def write_dataframe_to_mysql_database(self, df):
        "Если загружаем dataframe то колонка индексов должна соответствовать индексам из mysql"
        table_name = db_config.table_name
        sql_engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{db_config.password}@127.0.0.1/test', pool_recycle=3600)
        db_connection = sql_engine.connect()

        dtype = {
            'Id': sqlalchemy.types.INTEGER(),
            'Date': sqlalchemy.types.DATETIME(),
            'Name': sqlalchemy.types.VARCHAR(length=255),
            'Price_ZL': sqlalchemy.types.FLOAT(),
            'Price_EUR': sqlalchemy.types.FLOAT(),
            'Link': sqlalchemy.types.TEXT(), 
            'Department': sqlalchemy.types.VARCHAR(length=255), 
            'Project': sqlalchemy.types.VARCHAR(length=255),
            'Comments': sqlalchemy.types.TEXT(),
        }

        for i in range(len(df)):
            try:
                df.iloc[i:i+1].to_sql(name=table_name, con=db_connection, if_exists='append', dtype=dtype)
            except sqlalchemy.exc.IntegrityError: # пропускаем строки с одинаковыми индексами в таблице и базе данных
                pass #or any other action
        
        db_connection.close()

    def read_data_from_mysql(self):
        table_name = db_config.table_name
        sql_engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{db_config.password}@127.0.0.1/test', pool_recycle=3600)
        db_connection = sql_engine.connect()
        df = pd.read_sql(f'SELECT * FROM {table_name}', con=db_connection, index_col='Id')
        return df
