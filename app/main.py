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
        logger.info('class App')
        super().__init__()
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

if __name__ == '__main__':
    app = App()
    app.run_qt()
