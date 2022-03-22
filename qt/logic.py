from loguru import logger

import qt.procurement as qt_window


class BackgroundLogic:
    "Действия которые происходят после нажатия на кнопки главного меню"
    def __init__(self) -> None:
        logger.info('class AppLogic')
        self._press_procurement = None # еще не нажимали на кнопку Закупки в главном меню

    @property
    def press_procurement(self):
        if self._press_procurement is None: # если еще не нажимали на кнопку закупок
            self.main_window.hide()
        return self._press_procurement


class MainButtonsClick(BackgroundLogic):
    "Здесь объекты которые создаю после нажатия на кнопку главного меню"
    def __init__(self, main_window) -> None:
        logger.info('class MainButtonsClick')
        super().__init__()
        self.main_window = main_window
        self._procurement_form = None # таблица закупок
        self._procurement_btn_menu = None # меню кнопок для таблицы закупок

    def get_procurement_form(self):
        "Этот метод подключен к кнопке Закупки в главное меню"
        self.press_procurement # фиксируем нажатие на кнопку закупок
        self.procurement_form.show() # разворачиваю окно таблицы
        self.procurement_btn_menu.show() # разворачиваю кнопки управления

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
