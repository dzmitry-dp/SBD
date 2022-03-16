from loguru import logger

import qt.window as window


class AppLogic:
    def __init__(self) -> None:
        logger.info('class AppLogic')
        self._press_procurement = False # еще не нажимали на кнопку Закупки в главном меню

class MainButtonsClick(AppLogic):
    "Объект который создается после нажатия на кнопку меню"
    def __init__(self) -> None:
        logger.info('class MainButtonsClick')
        super().__init__()
        self._procurement_form = None # таблица закупок

    def get_procurement_form(self, screen_size):
        self._procurement_form = window.QtProcurementTableWindow(screen_size)
        self._procurement_form.show()
