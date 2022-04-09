from loguru import logger

import config
import db.config as db_config
from db.connect import connection_to_database

class ProcurementDataBaseQuery:
    def __init__(self):
        logger.info(f'class {self.__class__.__name__}')
        self.query = ''

    @connection_to_database
    def return_db_version(self):
        return "SELECT version();"
    
    @connection_to_database
    def create_table(self, data: dict = db_config.table):
        table_name: str = data['table_name']
        columns_and_types: dict = data['col_ty']

        for column in columns_and_types.keys():
            self.query += f"{column} {columns_and_types[column]}, "

        return f"CREATE TABLE IF NOT EXISTS {table_name}({self.query[:-2]});"

    @connection_to_database
    def write_values_to_the_table(self, data=None, table_name: str = db_config.table_name):
        table_name: str = table_name

        if data == None:
            columns_and_values: dict = db_config.example_values
        else:
            columns_and_values: dict = data

        columns = list(columns_and_values.keys())
        values = list(columns_and_values.values())
        return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"

    @connection_to_database
    def show_all_columns_from_table(self, table_name: str = db_config.table_name):
        columns = ', '.join(list(db_config.table['col_ty'].keys()))
        return f"SELECT {columns} FROM {table_name};"

    @connection_to_database
    def show_last_records(self, table_name=db_config.table_name, order_by=list(db_config.table['col_ty'].keys())[0], limit=config.TABLE_ROWS):
        return f"SELECT * FROM {table_name} ORDER BY {order_by} DESC LIMIT {limit}"

    @connection_to_database
    def show_tables_on_database(self):
        return "SHOW TABLES;"

    @connection_to_database
    def del_table(self, table_name=db_config.table_name):
        return f"DROP TABLE {table_name};"
