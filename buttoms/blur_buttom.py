from PyQt6.QtWidgets import QGraphicsBlurEffect, QPushButton
from PyQt6.QtCore import pyqtSlot

class BlurButton(QPushButton):
    def __init__(self, text, on_toggled):
        super().__init__(text)

        self.setCheckable(True)
        self.toggled.connect(on_toggled)

