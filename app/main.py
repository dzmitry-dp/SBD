import sys
from loguru import logger
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QPropertyAnimation

from qt.main_window import QtMainWindow
# from db.procurement import ProcurementDataBaseQuery, MySQLwithPandas

def _get_screen_size():
    # получаю данные о разрешении монитора
    # размер экрана компьютера 
    screen_geometry= QDesktopWidget().availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    return screen_width, screen_height

class App:
    def __init__(self) -> None:
        logger.info(f'class {self.__class__.__name__}')
        # создаю приложение и провожу настройки
        self.app = QApplication(sys.argv)
        # создаю главное окно
        self.main_window = QtMainWindow(*_get_screen_size())

    def run_qt(self):
        # программируем стартовую анимацию
        main_animation = QPropertyAnimation(self.main_window, b'windowOpacity')
        main_animation.setDuration(1000)  # Продолжительность: 1 секунда
        main_animation.setStartValue(0)
        main_animation.setEndValue(1)
        main_animation.start()

        self.main_window.show()
        sys.exit(self.app.exec_())

import pandas as pd
import sqlalchemy
import db.config as db_config

class MySQLwithPandas:
    def import_excel_file_to_mysql_database(self, database_name=db_config.database_name, table_name=db_config.table_name):
        "Если загружаем из excel то убираем индексы которые в таблице excel"
        df: pd.DataFrame = pd.read_excel('./static/procurement.xlsx', engine='openpyxl')
        raise NameError ('Исправь sql_engine = sqlalchemy.create_engine')
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
        raise NameError ('Следует внести изменения в sql_engine')
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

    def read_data_from_mysql(self, table_name=db_config.table_name):
        sql_engine = sqlalchemy.create_engine(f'postgresql://{db_config.user_name}:{db_config.password}@127.0.0.1/test', pool_recycle=3600)
        db_connection = sql_engine.connect()
        df = pd.read_sql(f'SELECT * FROM {table_name}', con=db_connection, index_col='Proc_Id')
        return df

if __name__ == '__main__':
    app = App()
    app.run_qt()
