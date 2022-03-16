from loguru import logger
from PyQt5.QtWidgets import QLabel, QPushButton

import config

class QtButtonElements:
    def __init__(self) -> None:
        logger.info('class QtButtonElements')

    def _create_button_widget(self):
        widget = QLabel(self)
        return widget

    def _create_qt_button(self, name):
        button = QPushButton(name, self)
        return button
    
    def init_button(self, name):
        widget = self._create_button_widget()
        button = self._create_qt_button(name)
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
                            "border :2px solid #0776A0;"
                            "}")
