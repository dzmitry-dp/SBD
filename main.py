"""
- Разворачиваем интерфейс
- Подключаемся к базам данных
"""
import sys
from loguru import logger
import pandas as pd
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtGui import QFont, QFontDatabase

import config
from qt.window import QtMainWindow
from db.connect import connection_to_database


class App:
    def __init__(self) -> None:
        logger.info('class App')
        super().__init__()
        # создаю приложение и провожу настройки
        self.app = QApplication(sys.argv)
        QFontDatabase.addApplicationFont(config.FONT_PATH)
        self.app.setFont(QFont( config.FONT_NAME , config.FONT_SIZE))
        screen_width, screen_height = self._get_screen_size()
        # разрешение монитора
        self.screen_size = (screen_width, screen_height)
        # центральная точка на мониторе
        self.center_screen_point = (int(screen_width/2), int(screen_height/2))
        # создаю главное окно
        self.main_window = QtMainWindow(screen_width, screen_height)

    def _get_screen_size(self):
        logger.info('class Screen')
        # размер экрана компьютера 
        screen_geometry= QDesktopWidget().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        return screen_width, screen_height

    def run_qt(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

class DataBaseQuery:
    def __init__(self):
        logger.info('class DataBaseConnect')
        self.query = ''

    @connection_to_database
    def create_table(self, data: dict):
        table_name: str = data['table_name']
        columns_and_types: dict = data['col_ty']

        for column in columns_and_types.keys():
            self.query += f"{column} {columns_and_types[column]}, "

        return f"CREATE TABLE IF NOT EXISTS {table_name} ({self.query[:-2]});"

    @connection_to_database
    def write_to_the_table(self, data):
        table_name: str = data['table_name']
        columns_and_values: dict = data['col_val']
        columns = list(columns_and_values.keys())
        values = list(columns_and_values.values())
        return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"

    @connection_to_database
    def show_all(self):
        return "SELECT * FROM test;"

    @connection_to_database
    def del_table(self):
        return "DROP TABLE test;"


if __name__ == '__main__':
    app = App()
    # db = DataBaseQuery()

    # create_new_table_data = {
    #     'table_name': 'test',
    #     'col_ty': {
    #         'id': 'INT NOT NULL AUTO_INCREMENT',
    #         'Date': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    #         'Name': 'VARCHAR(255)',
    #         'Price_ZL': 'FLOAT',
    #         'Price_EUR': 'FLOAT',
    #         'Link': 'TEXT', 
    #         'Department': 'VARCHAR(255)', 
    #         'Project': 'VARCHAR(255)',
    #         'Comments': 'TEXT, PRIMARY KEY (id)',
    #     }
    # }
    # db.create_table(data=create_new_table_data)

    # insert_new_raw_data = {
    #     'table_name': 'test',
    #     'col_val': {
    #         # 'Date': "'2022-03-03'",
    #         'Name': "'Трубка шланга для пылесоса с метражом 20мм длина 50 м'",
    #         'Price_ZL': '84.04',
    #         'Price_EUR': '64.33',
    #         'Link': "'https://allegro.pl/moje-allegro/zakupy/kupione/ddb72880-9b06-11ec-a466-1d12e6b7c649'", 
    #         'Department': "'Столярка'", 
    #         'Project': "'Reactor - Prague'",
    #         'Comments': "'Не выставляют фактуру'",
    #     }
    # }
    # db.write_to_the_table(data=insert_new_raw_data)

    # result = db.show_all()
    # df: pd.DataFrame = pd.read_excel('./static/procurement.xlsx', engine='openpyxl')

    # print(df)
    
    # db.del_table()
    # logger.info('Create app')
    app.run_qt()
