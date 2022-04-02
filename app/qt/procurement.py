import sys
from datetime import datetime, date
# from functools import partial
from loguru import logger
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import config
from qt.elements import QtButtonElements
from db.procurement_query import ProcurementDataBaseQuery

class TableWindowSize(QWidget):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.screen_size = main_window.screen_size
        self.procurement_table_window_size = self._calculation_procurement_table_window_size()

        self.current_width_point = 0 # переменная в которую записываю координату ширины, где должен начинаться новый виджет
        self.current_heigth_input_line = config.ID_INPUT_HEIGTH # переменная в которую записываю координату высоты, где должен начинаться новый виджет
        self.current_heigth_table = self.current_heigth_input_line * 18 # высота таблицы
        # высота области дополнительной информации
        self.current_heigth_additionally_information = self.procurement_table_window_size[1] - self.current_heigth_input_line - self.current_heigth_table

    def _calculation_procurement_table_window_size(self):
        "Расчитываю размер окна таблицы Закупки - A+props"
        return int(self.screen_size[0] * config.PROCENT_OF_WINDOW), int(self.screen_size[1] * config.PROCENT_OF_WINDOW)

class QtProcurementTableWindow(TableWindowSize):
    "Окно таблицы, которое появляется когда пользователь нажимает кнопку главного меню"
    def __init__(self, main_window) -> None:
        logger.info('class QtTableWindow')
        super().__init__(main_window)
        # создаем элементы интерфейса
        self.procurement_input_line = self._create_input_procurement_line() # полоса для ввода данных
        self.table_obj = self._create_table() # объект таблица
        self.additionally_information_obj = self._create_additionall_information()

        self._init_window()

    def _init_window(self):
        def _location_table_window_on_screen(width, heigth):
            "Вычисление центральной точки окна для объекта расположенного внутри этого окна"
            center_screen_point = (int(self.screen_size[0]/2), int(self.screen_size[1]/2))
            x = int(center_screen_point[0] - width/2)
            y = int(center_screen_point[1] - heigth/2)
            return x, y

        width, heigth = self.procurement_table_window_size
        start_point = _location_table_window_on_screen(width, heigth)
        x, y = start_point
        self.setGeometry(x, y, width, heigth)
        self.setWindowTitle(config.PROCUREMENT_WINDOW_TEXT)
        self.setWindowIcon(QIcon(config.PROCUREMENT_UPDATE_BTN))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint) # делаю не активной кнопку 'развернуть'

    def _create_input_procurement_line(self):
        "Последовательно создаем элементы для ввода данных. Каждый новый элемент отталкивается от координат предыдущего элемента"
        start_point = (0, 0)
        window_width = self.procurement_table_window_size[0]

        def _create_id_input():
            width = int(window_width*config.ID_PERCENT_OF_WIDTH)
            heigth = config.ID_INPUT_HEIGTH

            id_input_widget = QLabel(self)
            id_input_widget.resize(width, heigth)
            id_input_widget.move(start_point[0], start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            id_input = QLineEdit(self)
            id_input.setMaxLength(config.ID_MAX_SYMBOLS)
            id_input.resize(width, heigth)
            id_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            id_input.setPlaceholderText("Id")
            id_input.move(start_point[0], start_point[1])
            # id_input.setStyleSheet("background: transparent; border: none;")
            # id_input.setFocus()
            # id_input.clearFocus()

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='Id')
            self.current_width_point += width # точка где заканчивается этот виджет
            return id_input_widget, id_input
        
        def _crete_date_input():
            width = int(window_width*config.DATE_PERCENT_OF_WIDTH)
            heigth = config.DATE_INPUT_HEIGTH

            date_input_widget = QLabel(self)
            date_input_widget.resize(width, heigth)
            date_input_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            date_input = QLineEdit(self)
            date_input.setMaxLength(config.DATE_MAX_SYMBOLS)
            date_input.resize(width, heigth)
            date_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            date_input.setPlaceholderText(f"{date.today().strftime('%Y-%m-%d')}")
            date_input.move(start_point[0] + self.current_width_point, start_point[1])
            # date_input.setStyleSheet("background: transparent; border: none;")
            # id_input.setFocus()

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='Date')
            self.current_width_point += width # точка где заканчивается этот виджет
            return date_input_widget, date_input

        def _create_name_input():
            width = int(window_width*config.NAME_PERCENT_OF_WIDTH)
            heigth = config.NAME_INPUT_HEIGTH

            name_input_widget = QLabel(self)
            name_input_widget.resize(width, heigth)
            name_input_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            name_input = QLineEdit(self)
            name_input.setMaxLength(config.NAME_MAX_SYMBOLS)
            name_input.resize(width, heigth)
            name_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            name_input.setPlaceholderText("Name")
            name_input.move(start_point[0] + self.current_width_point, start_point[1])
            # date_input.setStyleSheet("background: transparent; border: none;")
            name_input.setFocus()

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='Name')
            self.current_width_point += width # точка где заканчивается этот виджет
            return name_input_widget, name_input

        def _create_price_zl_input():
            width = int(window_width*config.PRICE_ZL_PERCENT_OF_WIDTH)
            heigth = config.PRICE_ZL_INPUT_HEIGTH

            price_zl_input_widget = QLabel(self)
            price_zl_input_widget.resize(width, heigth)
            price_zl_input_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            price_zl_input = QLineEdit(self)
            price_zl_input.setMaxLength(config.PRICE_ZL_MAX_SYMBOLS)
            price_zl_input.resize(width, heigth)
            price_zl_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            price_zl_input.setPlaceholderText("ZL")
            price_zl_input.move(start_point[0] + self.current_width_point, start_point[1])
            # date_input.setStyleSheet("background: transparent; border: none;")
            # id_input.setFocus()

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='ZL')
            self.current_width_point += width # точка где заканчивается этот виджет
            return price_zl_input_widget, price_zl_input

        def _create_price_eur_input():
            width = int(window_width*config.PRICE_EUR_PERCENT_OF_WIDTH)
            heigth = config.PRICE_EUR_INPUT_HEIGTH

            price_eur_input_widget = QLabel(self)
            price_eur_input_widget.resize(width, heigth)
            price_eur_input_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            price_eur_input = QLineEdit(self)
            price_eur_input.setMaxLength(config.PRICE_EUR_MAX_SYMBOLS)
            price_eur_input.resize(width, heigth)
            price_eur_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру
            price_eur_input.setPlaceholderText("EUR")
            price_eur_input.move(start_point[0] + self.current_width_point, start_point[1])
            # date_input.setStyleSheet("background: transparent; border: none;")
            # id_input.setFocus()

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='EUR')
            self.current_width_point += width # точка где заканчивается этот виджет
            return price_eur_input_widget, price_eur_input

        def _create_link_input():
            width = int(window_width*config.LINK_PERCENT_OF_WIDTH)
            heigth = config.LINK_INPUT_HEIGTH

            link_input_widget = QLabel(self)
            link_input_widget.resize(width, heigth)
            link_input_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            link_input = QLineEdit(self)
            link_input.setMaxLength(config.LINK_MAX_SYMBOLS)
            link_input.resize(width, heigth)
            link_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            link_input.setPlaceholderText("http://...")
            link_input.move(start_point[0] + self.current_width_point, start_point[1])
            # date_input.setStyleSheet("background: transparent; border: none;")
            # id_input.setFocus()

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='Link')
            self.current_width_point += width # точка где заканчивается этот виджет
            return link_input_widget, link_input

        def _create_department_drop_btn():
            width = int(window_width*config.DEPARTMENT_PERCENT_OF_WIDTH)
            heigth = config.DEPARTMENT_BTN_HEIGTH

            department_widget = QLabel(self)
            department_widget.resize(width, heigth)
            department_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            drop_btn = QComboBox(self)
            for department in config.DEPARTMENTS:
                drop_btn.addItem(department)

            drop_btn.resize(width, heigth)
            drop_btn.move(start_point[0] + self.current_width_point, start_point[1])

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='Department')
            self.current_width_point += width # точка где заканчивается этот виджет
            return department_widget, drop_btn

        def _create_project_drop_btn():
            width = int(window_width*config.PROJECT_PERCENT_OF_WIDTH)
            heigth = config.PROJECT_BTN_HEIGTH

            project_widget = QLabel(self)
            project_widget.resize(width, heigth)
            project_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            drop_btn = QComboBox(self)
            for project in config.PROJECTS:
                drop_btn.addItem(project)

            drop_btn.resize(width, heigth)
            drop_btn.move(start_point[0] + self.current_width_point, start_point[1])

            # self._create_head_of_table(width=width, heigth=heigth, point=start_point, text='Project')
            self.current_width_point += width # точка где заканчивается этот виджет
            return project_widget, drop_btn

        def _create_comment_input_line():
            width = int(window_width*config.COMMENT_PERCENT_OF_WIDTH)
            heigth = config.COMMENT_INPUT_HEIGTH

            comment_input_widget = QLabel(self)
            comment_input_widget.resize(width, heigth)
            comment_input_widget.move(start_point[0] + self.current_width_point, start_point[1])
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            comment_input = QLineEdit(self)
            comment_input.setMaxLength(config.COMMENT_MAX_SYMBOLS)
            comment_input.resize(width, heigth)
            comment_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            comment_input.setPlaceholderText("We are waiting your comments ...")
            comment_input.move(start_point[0] + self.current_width_point, start_point[1])
            # date_input.setStyleSheet("background: transparent; border: none;")
            # id_input.setFocus()

            return comment_input_widget, comment_input

        id_widget_and_input_line = _create_id_input()
        date_widget_and_input_line = _crete_date_input()
        name_widget_and_input_line = _create_name_input()
        price_zl_widget_and_input_line = _create_price_zl_input()
        price_eur_widget_and_input_line = _create_price_eur_input()
        link_widget_and_input_line = _create_link_input()
        department_widget_and_drop_btn = _create_department_drop_btn()
        project_widget_and_drop_btn = _create_project_drop_btn()
        comment_widget_and_input_line = _create_comment_input_line()

        return id_widget_and_input_line, date_widget_and_input_line, \
            name_widget_and_input_line, price_zl_widget_and_input_line, \
            price_eur_widget_and_input_line, link_widget_and_input_line, \
            department_widget_and_drop_btn, project_widget_and_drop_btn, \
            comment_widget_and_input_line

    def _create_table(self):
        def add_row_in_table(row, row_number):
            for i, item in enumerate(row):
                if isinstance(item, datetime):
                    new_item = QTableWidgetItem(item.strftime('%Y-%m-%d'))
                else:
                    new_item = QTableWidgetItem(str(item))
                table_widget.setItem(row_number, i, new_item)

        table_widget = QTableWidget(config.TABLE_ROWS, config.TABLE_COLUMNS, self)
        table_widget.resize(self.procurement_table_window_size[0], self.current_heigth_table)
        table_widget.move(0, self.current_heigth_input_line)

        db_connect = ProcurementDataBaseQuery()
        new_table_if_not_exists = db_connect.create_table()
        test_raw = db_connect.write_values_to_the_table()
        last_records = db_connect.show_last_records()


        for i, row in enumerate(last_records):
            add_row_in_table(row, i)

        table_widget.setColumnWidth(0, int(self.procurement_table_window_size[0]*config.ID_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(1, int(self.procurement_table_window_size[0]*config.DATE_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(2, int(self.procurement_table_window_size[0]*config.NAME_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(3, int(self.procurement_table_window_size[0]*config.PRICE_ZL_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(4, int(self.procurement_table_window_size[0]*config.PRICE_EUR_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(5, int(self.procurement_table_window_size[0]*config.LINK_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(6, int(self.procurement_table_window_size[0]*config.DEPARTMENT_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(7, int(self.procurement_table_window_size[0]*config.PROJECT_PERCENT_OF_WIDTH))
        table_widget.setColumnWidth(8, int(self.procurement_table_window_size[0]*config.COMMENT_PERCENT_OF_WIDTH))

        for i in range(0, config.TABLE_ROWS):
            table_widget.setRowHeight(i, self.current_heigth_input_line)

        # скрываю имена колонок и нумерацию строк
        header = table_widget.horizontalHeader() # имена столбцов
        header.hide()
        rows_numbers = table_widget.verticalHeader() # нумерация строк
        rows_numbers.hide()

        return table_widget

    def _create_additionall_information(self):
        def center_location_on_the_window(_object, _self):
            "Вычисление центральной точки окна для объекта расположенного внутри этого окна"
            window_size = _self.geometry()
            element_size = _object.geometry()
            x = int(window_size.width()/2 - element_size.width()/2)
            y = int(window_size.height()/2 - element_size.height()/2)
            return x, y

        width, heigth = self.procurement_table_window_size
        additionall_information = QLabel(self)
        additionall_information.resize(width, heigth - self.current_heigth_input_line - self.current_heigth_table)
        additionall_information.move(0, self.current_heigth_input_line + self.current_heigth_table)
        # additionall_information.setStyleSheet("background: #5FC0CE; border: 2px solid;")

        header = QLabel(additionall_information)
        header.setMinimumHeight(50)
        x, y = center_location_on_the_window(header, additionall_information)
        header.move(x, 0)
        header.setText('Additionall Information')

        balance_zl = QLabel(additionall_information)
        balance_zl.setMinimumHeight(50)
        balance_zl.setMinimumWidth(50)
        balance_zl.move(100, 50)
        balance_zl.setText('Balance: 40 000 zl')

        balance_eur = QLabel(additionall_information)
        balance_eur.setMinimumHeight(50)
        balance_eur.setMinimumWidth(50)
        balance_eur.move(100, 100)
        balance_eur.setText('Balance: 10 000 eur')

        balance_1 = QLabel(additionall_information)
        balance_1.setMinimumHeight(50)
        balance_1.setMinimumWidth(50)
        balance_1.move(self.procurement_table_window_size[0] - 250, 50)
        balance_1.setText('40 000 zl : Balance')

        balance_2 = QLabel(additionall_information)
        balance_2.setMinimumHeight(50)
        balance_2.setMinimumWidth(50)
        balance_2.move(self.procurement_table_window_size[0] - 250, 100)
        balance_2.setText('10 000 eur : Balance')

        message = QLabel(additionall_information)
        message.setMinimumHeight(50)
        x, y = center_location_on_the_window(message, additionall_information)
        message.move(x - 30, y + 50)
        message.setText('"Денег нет, но вы держитесь!"')

    def closeEvent(self, event):
        "Когда пользователь закрыл окно таблицы закупок"
        # self.main_window.start_animation.start()
        self.main_window.show()

class QtProcurementButtonsMenu(QWidget, QtButtonElements):
    "Кнопки которые использую для управления таблицей заказов"
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.screen_size = main_window.screen_size

        self._update = None # "скачать снова" данные с текущими настройками

        self._init_window()

    @property
    def update(self):
        if self._update is None:
            self._update = self.init_button(name='') # возвращает widget + button
            for btn in self._update:
                btn.resize(*config.UPDATE_BTN_SIZE)
                btn.move(0, 0)
            self._set_procurement_sheet_menu_btn(self._update, config.PROCUREMENT_UPDATE_BTN)
        return self._update

    def _init_window(self):
        screen_width = self.screen_size[0]
        screen_height = self.screen_size[1]
        start_point = (screen_width - config.UPDATE_BTN_SIZE[0], int(screen_height/2) - int(config.UPDATE_BTN_SIZE[1]/2))
        self.setGeometry(*start_point, *config.PROCURUMENT_MENU_WINDOW_SIZE)
        self.setWindowFlags(Qt.FramelessWindowHint) # убираю верхнюю панель окна 
        self.setWindowFlag(Qt.WindowStaysOnTopHint) # приложение поверх других окон

        # подключаю кнопки
        self.update[1].clicked.connect(sys.exit)
