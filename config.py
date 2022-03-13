def center_location_on_the_window(_object, self):
    "Вычисление центральной точки окна для объекта расположенного внутри этого окна"
    window_size = self.geometry()
    element_size = _object.geometry()
    x = int(window_size.width()/2 - element_size.width()/2)
    y = int(window_size.height()/2 - element_size.height()/2)
    return x, y

START_POINT_X_Y = [0,0]
MENU_BTN_SIZE = (150, 150)
MAIN_WINDOW_SIZE = (MENU_BTN_SIZE[0], 7 * MENU_BTN_SIZE[1])

ICO_DOC_BTN = './static/doc.png'
ICO_PROJ_BTN = './static/proj.png'
ICO_ATTEND_BTN = './static/attendance.png'
ICO_PROC_BTN = './static/procurement.png'
ICO_CATEGORIES_BTN = './static/categories.png'
ICO_CUSTOM_BTN = './static/custom.png'

FONT_NAME = 'Hey Comic'
FONT_PATH = './static/HeyComic.ttf'
FONT_SIZE = 16

