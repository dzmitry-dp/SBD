"""
- Разворачиваем интерфейс
- Подключаемся к базам данных
"""
import sys
from loguru import logger
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtGui import QFont, QFontDatabase

import config
from qt.window import QtMainWindow
from db.procurement import ProcurementDataBaseQuery, MySQLwithPandas


class App:
    def __init__(self) -> None:
        logger.info('class App')
        super().__init__()
        # создаю приложение и провожу настройки
        self.app = QApplication(sys.argv)
        # QFontDatabase.addApplicationFont(config.FONT_PATH)
        # self.app.setFont(QFont( config.FONT_NAME , config.FONT_SIZE))
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

if __name__ == '__main__':
    app = App()
    # db = ProcurementDataBaseQuery()
    # df = MySQLwithPandas()

    app.run_qt()
