class AppLogic:
    def __init__(self) -> None:
        self._press_procurement = False # еще не нажимали на кнопку Закупки в главном меню

class MainButtonsClick(AppLogic):
    def __init__(self) -> None:
        super().__init__()

    def get_procurement_form(self):
        print('Открывается таблица закупок')
        self._press_procurement = True
