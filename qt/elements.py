from PyQt5.QtWidgets import QLabel, QPushButton

import config

class QtButtonElements:
    def __init__(self) -> None:
        self._btn_count = 0 # считаю количество кнопок

    def _create_button_widget(self):
        widget = QLabel(self)
        self._set_btn_size(widget)
        return widget

    def _create_qt_button(self, name):
        button = QPushButton(name, self)
        self._set_btn_size(button)
        return button
    
    def _set_btn_size(self, element):
        element.resize(*config.MENU_BTN_SIZE) # считываю размеры кнопок
        x, y = config.MENU_BTN_SIZE
        element.move(0, y * self._btn_count)

    def init_button(self, name):
        widget = self._create_button_widget()
        button = self._create_qt_button(name)
        self._btn_count += 1
        return widget, button

    def _set_style_sheet(self, obj, ico_path):
        widget = obj[0]
        button = obj[1]
        widget.setStyleSheet("QLabel"
                                  "{"
                                  f"background-image: url({ico_path});"
                                  "}")
        button.setStyleSheet("QPushButton"
                            "{"
                            f"background: transparent;"
                            "}"
                            "QPushButton::hover"
                            "{"
                            "border :3px solid #0776A0;"
                            "}"
                            "QPushButton::focus"
                            "{"
                            "border :3px solid #0776A0;"
                            "}")
