import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

import config
from qt.elements import QtButtonElements
from logic import MainButtonsClick

btn_click_logic = MainButtonsClick()

class QtMainWindow(QWidget, QtButtonElements):
    def __init__(self, screen_width, screen_height):
        super().__init__()
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
            self._set_style_sheet(self._project_btn, config.ICO_PROJ_BTN)
        return self._project_btn

    @property
    def attendance_btn(self):
        'Кнопка для просмотра посещаемости'
        if self._attendance_btn is None:
            self._attendance_btn = self.init_button(name='') # возвращает widget + button
            self._set_style_sheet(self._attendance_btn, config.ICO_ATTEND_BTN)
        return self._attendance_btn

    @property
    def procurement_btn(self):
        'Кнопка которая ведет на таблицу закупок'
        if self._procurement_btn is None:
            self._procurement_btn = self.init_button(name='') # возвращает widget + button
            self._set_style_sheet(self._procurement_btn, config.ICO_PROC_BTN)
        return self._procurement_btn

    @property
    def categories_btn(self):
        'Таблица сформированная по категориям'
        if self._categories_btn is None:
            self._categories_btn = self.init_button(name='') # возвращает widget + button
            self._set_style_sheet(self._categories_btn, config.ICO_CATEGORIES_BTN)
        return self._categories_btn

    @property
    def documentation_btn(self):
        'Таблица ссылок на документацию'
        if self._documentation_btn is None:
            self._documentation_btn = self.init_button(name='') # возвращает widget + button
            self._set_style_sheet(self._documentation_btn, config.ICO_DOC_BTN)
        return self._documentation_btn

    @property
    def custom_btn(self):
        'Таблица которую формирует сам пользователь'
        if self._custom_btn is None:
            self._custom_btn = self.init_button(name='') # возвращает widget + button
            self._set_style_sheet(self._custom_btn, config.ICO_CUSTOM_BTN)
        return self._custom_btn

    @property
    def exit_btn(self):
        if self._exit_btn is None:
            self._exit_btn = self.init_button(name='Exit') # возвращает widget + button
        return self._exit_btn

    def _init_window(self, screen_width, screen_height):
        start_point = (screen_width - config.MENU_BTN_SIZE[0], int(screen_height/2) - int(config.MAIN_WINDOW_SIZE[1]/2))
        self.setGeometry(*start_point, *config.MAIN_WINDOW_SIZE)
        self.setWindowFlags(Qt.FramelessWindowHint) # убираю верхнюю панель экрана 
        self.setWindowFlag(Qt.WindowStaysOnTopHint) # приложение поверх других окон

        # подключаю кнопки
        self.project_btn
        self.attendance_btn
        self.procurement_btn[1].clicked.connect(btn_click_logic.get_procurement_form)
        self.categories_btn
        self.documentation_btn
        self.custom_btn
        self.exit_btn[1].clicked.connect(sys.exit)
