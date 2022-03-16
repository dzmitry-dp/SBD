import sys
from functools import partial
from loguru import logger
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QIcon

import config
from qt.elements import QtButtonElements
from qt.logic import MainButtonsClick

btn_click_logic = MainButtonsClick()

class QtMainWindow(QWidget, QtButtonElements):
    def __init__(self, screen_width, screen_height):
        logger.info('class QtMainWindow')
        super().__init__()
        # Класс анимации прозрачности окна
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(1000)        # Продолжительность: 1 секунда
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        self.screen_size = None

        # отрисовываю элементы
        self._project_btn = None
        self._attendance_btn = None
        self._procurement_btn = None
        self._categories_btn = None
        self._documentation_btn = None
        self._custom_btn = None
        self._exit_btn = None
    
        self._init_window(screen_width, screen_height)

    @property
    def project_btn(self):
        'Кнопка по нажатию на которую направляю на таблицу, которая формируется относительно проекта'
        if self._project_btn is None:
            self._project_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._project_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 0)
            self._set_style_sheet(self._project_btn, config.ICO_PROJ_BTN)
        return self._project_btn

    @property
    def attendance_btn(self):
        'Кнопка для просмотра посещаемости'
        if self._attendance_btn is None:
            self._attendance_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._attendance_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 1)
            self._set_style_sheet(self._attendance_btn, config.ICO_ATTEND_BTN)
        return self._attendance_btn

    @property
    def procurement_btn(self):
        'Кнопка которая ведет на таблицу закупок'
        if self._procurement_btn is None:
            self._procurement_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._procurement_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 2)
            self._set_style_sheet(self._procurement_btn, config.ICO_PROC_BTN)
        return self._procurement_btn

    @property
    def categories_btn(self):
        'Таблица сформированная по категориям'
        if self._categories_btn is None:
            self._categories_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._categories_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 3)
            self._set_style_sheet(self._categories_btn, config.ICO_CATEGORIES_BTN)
        return self._categories_btn

    @property
    def documentation_btn(self):
        'Таблица ссылок на документацию'
        if self._documentation_btn is None:
            self._documentation_btn = self.init_button(name='') # возвращает widget + button
            self._documentation_btn[0].resize(*config.MAIN_MENU_BTN_SIZE)
            self._documentation_btn[0].move(0, config.MAIN_MENU_BTN_SIZE[1] * 4)
            self._documentation_btn[1].resize(*config.MAIN_MENU_BTN_SIZE)
            self._documentation_btn[1].move(0, config.MAIN_MENU_BTN_SIZE[1] * 4)
            self._set_style_sheet(self._documentation_btn, config.ICO_DOC_BTN)
        return self._documentation_btn

    @property
    def custom_btn(self):
        'Таблица которую формирует сам пользователь'
        if self._custom_btn is None:
            self._custom_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._custom_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 5)
            self._set_style_sheet(self._custom_btn, config.ICO_CUSTOM_BTN)
        return self._custom_btn

    @property
    def exit_btn(self):
        if self._exit_btn is None:
            self._exit_btn = self.init_button(name='Exit') # возвращает widget + button
            self._exit_btn[1].setStyleSheet("QPushButton"
                                  "{"
                                  "color: red;"
                                  "}")
            for btn in self._exit_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 6)
        return self._exit_btn

    def _init_window(self, screen_width, screen_height):
        # вычисляю геометрию откна
        self.screen_size = (screen_width, screen_height)
        start_point = (screen_width - config.MAIN_MENU_BTN_SIZE[0], int(screen_height/2) - int(config.MAIN_WINDOW_SIZE[1]/2))
        self.setGeometry(*start_point, *config.MAIN_WINDOW_SIZE)
        self.setWindowFlags(Qt.FramelessWindowHint) # убираю верхнюю панель окна 
        self.setWindowFlag(Qt.WindowStaysOnTopHint) # приложение поверх других окон

        # подключаю кнопки
        self.project_btn
        self.attendance_btn
        self.procurement_btn[1].clicked.connect(partial(btn_click_logic.get_procurement_form, self.screen_size))
        self.categories_btn
        self.documentation_btn
        self.custom_btn
        self.exit_btn[1].clicked.connect(sys.exit)


class QtProcurementTableWindow(QWidget):
    "Окно таблиц, которое появляется когда пользователь нажимает кнопку главного меню"
    def __init__(self, screen_size) -> None:
        logger.info('class QtTableWindow')
        super().__init__()
        self.screen_size = screen_size
        self.table_window_size = self._calculation_table_window_size()
        self.center_screen_point = (int(screen_size[0]/2), int(screen_size[1]/2))
        self.start_point = self._location_table_window_on_screen(self.table_window_size[0], self.table_window_size[1])
        self._init_window()

    def _init_window(self):
        width , heigth = self.table_window_size
        x, y = self.start_point
        self.setGeometry(x, y, width, heigth)
        self.setWindowTitle('Закупки A+props')
        self.setWindowIcon(QIcon('.\\static\\procurement.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint) # делаю не активной кнопку 'развернуть'

    def _location_table_window_on_screen(self, width, heigth):
        "Вычисление центральной точки окна для объекта расположенного внутри этого окна"
        x = int(self.center_screen_point[0] - width/2)
        y = int(self.center_screen_point[1] - heigth/2)
        return x, y
    
    def _calculation_table_window_size(self):
        return int(self.screen_size[0] * config.PROCENT_OF_WINDOW), int(self.screen_size[1] * config.PROCENT_OF_WINDOW)
