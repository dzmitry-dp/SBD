# MySQL database
########
table = {
    'table_name': 'test',
    'col_ty': {
        'Id': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
        'Date': 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP',
        'Name': 'VARCHAR(255)',
        'Price_ZL': 'FLOAT',
        'Price_EUR': 'FLOAT',
        'Link': 'TEXT', 
        'Department': 'VARCHAR(255)', 
        'Project': 'VARCHAR(255)',
        'Comments': 'VARCHAR(255)',
        }
    }

example_values = {
        'Date': "'2022-03-03'",
        'Name': "'Трубка шланга для пылесоса с метражом 20мм длина 50 м'",
        'Price_ZL': '84.04',
        'Price_EUR': '64.33',
        'Link': "'https://allegro.pl/moje-allegro/zakupy/kupione/ddb72880-9b06-11ec-a466-1d12e6b7c649'", 
        'Department': "'Столярка'", 
        'Project': "'Reactor - Prague'",
        'Comments': "'Не выставляют фактуру'",
    }

# main window
########
# START_POINT_X_Y = [0,0]
MAIN_MENU_BTN_SIZE = (150, 150)
MAIN_WINDOW_SIZE = (MAIN_MENU_BTN_SIZE[0], 7 * MAIN_MENU_BTN_SIZE[1])

ICO_DOC_BTN = './static/doc.png'
ICO_PROJ_BTN = './static/proj.png'
ICO_ATTEND_BTN = './static/attendance.png'
ICO_PROC_BTN = './static/procurement.png'
ICO_CATEGORIES_BTN = './static/categories.png'
ICO_CUSTOM_BTN = './static/custom.png'

FONT_NAME = 'Apple Garamond'
FONT_PATH = './static/AppleGaramond.ttf'
FONT_SIZE = 16
########

# provurement table window
########
PROCENT_OF_WINDOW = 0.8 # размер окна таблицы в % от всего экрана монитора
########

# input line procurement
########
ID_INPUT_HEIGTH = 50
ID_PERCENT_OF_WIDTH = 0.05 # 5% от всей ширины окна таблицы
ID_MAX_SYMBOLS = 5

DATE_INPUT_HEIGTH = ID_INPUT_HEIGTH
DATE_PERCENT_OF_WIDTH = 0.07 # 7% от всей ширины окна таблицы
DATE_MAX_SYMBOLS = 10

NAME_INPUT_HEIGTH = DATE_INPUT_HEIGTH
NAME_PERCENT_OF_WIDTH = 0.23 # 17% от всей ширины окна таблицы
NAME_MAX_SYMBOLS = 255

PRICE_ZL_INPUT_HEIGTH = NAME_INPUT_HEIGTH
PRICE_ZL_PERCENT_OF_WIDTH = 0.05 # 5% от всей ширины окна таблицы
PRICE_ZL_MAX_SYMBOLS = 5

PRICE_EUR_INPUT_HEIGTH = PRICE_ZL_INPUT_HEIGTH
PRICE_EUR_PERCENT_OF_WIDTH = 0.05 # 5% от всей ширины окна таблицы
PRICE_EUR_MAX_SYMBOLS = 5

LINK_INPUT_HEIGTH = PRICE_EUR_INPUT_HEIGTH
LINK_PERCENT_OF_WIDTH = 0.15 # 20% от всей ширины окна таблицы
LINK_MAX_SYMBOLS = 255

DEPARTMENT_BTN_HEIGTH = LINK_INPUT_HEIGTH
DEPARTMENT_PERCENT_OF_WIDTH = 0.11 # 15% от всей ширины окна таблицы

PROJECT_BTN_HEIGTH = DEPARTMENT_BTN_HEIGTH
PROJECT_PERCENT_OF_WIDTH = 0.11 # 15% от всей ширины окна таблицы

COMMENT_INPUT_HEIGTH= 50
COMMENT_PERCENT_OF_WIDTH = 1 - PROJECT_PERCENT_OF_WIDTH -\
    DEPARTMENT_PERCENT_OF_WIDTH - LINK_PERCENT_OF_WIDTH -\
    PRICE_EUR_PERCENT_OF_WIDTH - PRICE_ZL_PERCENT_OF_WIDTH -\
    NAME_PERCENT_OF_WIDTH - DATE_PERCENT_OF_WIDTH -\
    ID_PERCENT_OF_WIDTH # 100% от всей ширины окна таблицы
COMMENT_MAX_SYMBOLS = 255
########

# procurement table
########
TABLE_ROWS = 17
TABLE_COLUMNS = len(table['col_ty'])

DEPARTMENTS = [
    'None',
    'Бутафория',
    'Декор', 
    'Столярка',
    'Мебель',
    'Стены',
    'Отделочные',
    'Электроника',
    'Диджитал',
    'Готовое',
    'Общие',
    'Печать',
    'Офис',
    'Выезд',
    ]

PROJECTS = [
    'None',
    'Butcher 3 - Metz',
    'Hades - Metz',
    'Freddy - Nice',
    'Eldorado - Belgium',
    'Prison - Nancy',
    'VR',
    'FunConstructor',
    'Офис',
    'Toystore -  Ireland',
    'Props - UAE',
    'Time Machine - Prague',
    'Quiz - Portable',
    'ПОСТОБСЛУЖИВАНИЕ',
    'Matrix - Prague',
    'Toystore -  Wroclaw',
    'Toystore -  Malaysia',
    'Reactor - Prague',
    'Hangover - Nancy',
    'Kvantario - Benesov',
]
