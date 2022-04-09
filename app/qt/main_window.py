from functools import partial
from loguru import logger
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

import config
from qt.elements import QtButtonElements
from qt.logic import MainButtonsClick


class QtMainWindow(QWidget, QtButtonElements):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        logger.info(f'class {self.__class__.__name__}')
        self.screen_size = (screen_width, screen_height)

        # отрисованные элементы
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
            self._set_main_button_style_sheet(self._project_btn, config.ICO_PROJ_BTN)
        return self._project_btn

    @property
    def attendance_btn(self):
        'Кнопка для просмотра посещаемости'
        if self._attendance_btn is None:
            self._attendance_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._attendance_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 1)
            self._set_main_button_style_sheet(self._attendance_btn, config.ICO_ATTEND_BTN)
        return self._attendance_btn

    @property
    def procurement_btn(self):
        'Кнопка которая ведет на таблицу закупок'
        if self._procurement_btn is None:
            self._procurement_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._procurement_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 2)
            self._set_main_button_style_sheet(self._procurement_btn, config.ICO_PROC_BTN)
        return self._procurement_btn

    @property
    def categories_btn(self):
        'Таблица сформированная по категориям'
        if self._categories_btn is None:
            self._categories_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._categories_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 3)
            self._set_main_button_style_sheet(self._categories_btn, config.ICO_CATEGORIES_BTN)
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
            self._set_main_button_style_sheet(self._documentation_btn, config.ICO_DOC_BTN)
        return self._documentation_btn

    @property
    def custom_btn(self):
        'Таблица которую формирует сам пользователь'
        if self._custom_btn is None:
            self._custom_btn = self.init_button(name='') # возвращает widget + button
            for btn in self._custom_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 5)
            self._set_main_button_style_sheet(self._custom_btn, config.ICO_CUSTOM_BTN)
        return self._custom_btn

    @property
    def exit_btn(self):
        if self._exit_btn is None:
            self._exit_btn = self.init_button(name='') # возвращает widget + button
            self._exit_btn[1].setFocus()
            for btn in self._exit_btn:
                btn.resize(*config.MAIN_MENU_BTN_SIZE)
                btn.move(0, config.MAIN_MENU_BTN_SIZE[1] * 6)
            self._set_main_button_style_sheet(self._exit_btn, config.ICO_EXIT_BTN)
        return self._exit_btn

    def _init_window(self, screen_width, screen_height):
        # вычисляю геометрию окна
        start_point = (screen_width - config.MAIN_MENU_BTN_SIZE[0], int(screen_height/2) - int(config.MAIN_WINDOW_SIZE[1]/2))
        self.setGeometry(*start_point, *config.MAIN_WINDOW_SIZE)
        self.setWindowFlags(Qt.FramelessWindowHint) # убираю верхнюю панель окна 
        self.setWindowFlag(Qt.WindowStaysOnTopHint) # приложение поверх других окон

        # создаю объкт который контролирует нажатие кнопок главного окна
        btn_click_logic = MainButtonsClick(self)

        # подключаю кнопки
        self.project_btn
        self.attendance_btn
        self.procurement_btn[1].clicked.connect(partial(btn_click_logic.get_procurement_form))
        self.categories_btn
        self.documentation_btn
        self.custom_btn
        self.exit_btn[1].clicked.connect(partial(btn_click_logic.shut_down))
