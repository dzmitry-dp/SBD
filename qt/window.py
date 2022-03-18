import sys
from datetime import datetime, date
from functools import partial
from loguru import logger
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QIcon

import config
from qt.elements import QtButtonElements
from qt.logic import MainButtonsClick
from db.procurement import ProcurementDataBaseQuery

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
                                  "font-size:40px;"
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
        self.procurement_table_window_size = self._calculation_procurement_table_window_size()

        self.current_width_point = 0 # переменная в которую записываю координату ширины, где должен начинаться новый виджет
        self.current_heigth_point = config.ID_INPUT_HEIGTH # переменная в которую записываю координату высоты, где должен начинаться новый виджет
        # создаем элементы которые заполняет пользователь
        self.procurement_input = self._create_input_pricurement_line()
        self.table = self._create_table()
        self.table.show()

        self._init_window()

    def _init_window(self):
        width, heigth = self.procurement_table_window_size
        start_point = self._location_table_window_on_screen(self.procurement_table_window_size[0], self.procurement_table_window_size[1])
        x, y = start_point
        self.setGeometry(x, y, width, heigth)
        self.setWindowTitle('Закупки - A+props')
        self.setWindowIcon(QIcon('.\\static\\procurement.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint) # делаю не активной кнопку 'развернуть'
        self.setFocus()

    def _location_table_window_on_screen(self, width, heigth):
        "Вычисление центральной точки окна для объекта расположенного внутри этого окна"
        center_screen_point = (int(self.screen_size[0]/2), int(self.screen_size[1]/2))
        x = int(center_screen_point[0] - width/2)
        y = int(center_screen_point[1] - heigth/2)
        return x, y
    
    def _calculation_procurement_table_window_size(self):
        "Расчитываю размер окна таблицы Закупки - A+props"
        return int(self.screen_size[0] * config.PROCENT_OF_WINDOW), int(self.screen_size[1] * config.PROCENT_OF_WINDOW)

    def _create_input_pricurement_line(self):
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
            drop_btn.addItem("motif")
            drop_btn.addItem("Windows")
            drop_btn.addItem("cde")
            drop_btn.addItem("Plastique")
            drop_btn.addItem("Cleanlooks")
            drop_btn.addItem("windowsvista")
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
            drop_btn.addItem("motif")
            drop_btn.addItem("Windows")
            drop_btn.addItem("cde")
            drop_btn.addItem("Plastique")
            drop_btn.addItem("Cleanlooks")
            drop_btn.addItem("windowsvista")
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
            comment_input_widget.move(0, config.ID_INPUT_HEIGTH)
            # id_input_widget.setStyleSheet(f"background-image: url({config.PASSWORD_PNG});")

            comment_input = QLineEdit(self)
            comment_input.setMaxLength(config.COMMENT_MAX_SYMBOLS)
            comment_input.resize(width, heigth)
            comment_input.setAlignment(Qt.AlignCenter) # печатаю символы по центру 
            comment_input.setPlaceholderText("We are waiting your comments ...")
            comment_input.move(0, config.ID_INPUT_HEIGTH)
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

    # def _create_head_of_table(self, width, heigth, point, text):
    #     header = QLabel(self)
    #     header.setAlignment(Qt.AlignCenter)
    #     header.resize(width, heigth)
    #     header.move(point[0] + self.current_width_point, point[1])
    #     header.setText(text)

    def _create_table(self):
        def add_row_in_table(row, row_number):
            for i, item in enumerate(row):
                if isinstance(item, datetime):
                    new_item = QTableWidgetItem(item.strftime('%Y-%m-%d'))
                else:
                    new_item = QTableWidgetItem(str(item))
                table_widget.setItem(row_number, i, new_item)

        table_widget = QTableWidget(20, 9, self)
        table_widget.resize(self.procurement_table_window_size[0], self.procurement_table_window_size[1] - self.current_heigth_point*2)
        table_widget.move(0, self.current_heigth_point*3)

        db_connect = ProcurementDataBaseQuery()
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
        header = table_widget.horizontalHeader()
        header.hide()
        rows_numbers = table_widget.verticalHeader()
        rows_numbers.hide()

        return table_widget

    