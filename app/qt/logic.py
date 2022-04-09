import sys
from loguru import logger

import qt.procurement as qt_window


class BackgroundLogic:
    "Действия которые происходят после нажатия на кнопки главного меню"
    def __init__(self) -> None:
        logger.info(f'class {self.__class__.__name__}')
        self._press_procurement = None # еще не нажимали на кнопку Закупки в главном меню

    @property
    def press_procurement(self):
        if self._press_procurement is None:
            self.main_window.hide()
            self._press_procurement = True
        return self._press_procurement


class MainButtonsClick(BackgroundLogic):
    "Здесь создаю объекты которые должны появиться после нажатия на кнопку главного меню"
    def __init__(self, main_window) -> None:
        super().__init__()
        logger.info(f'class {self.__class__.__name__}')
        self.main_window = main_window
        self._procurement_form = None # таблица закупок
        self._procurement_btn_menu = None # меню кнопок для таблицы закупок

    @property
    def procurement_form(self):
        if self._procurement_form is None:
            self._procurement_form = qt_window.QtProcurementTableWindow(self.main_window)
        return self._procurement_form

    @property
    def procurement_btn_menu(self):
        if self._procurement_btn_menu is None:
            self._procurement_btn_menu = qt_window.QtProcurementButtonsMenu(self.main_window)
        return self._procurement_btn_menu

    def get_procurement_form(self):
        "Этот метод подключен к кнопке Закупки в главное меню"
        self.press_procurement # фиксируем нажатие на кнопку закупок
        self.procurement_form.show() # разворачиваю окно таблицы
        self.procurement_btn_menu.show() # разворачиваю кнопки управления

    def shut_down(self):
        sys.exit()