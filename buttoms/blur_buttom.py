from PyQt6.QtWidgets import QGraphicsBlurEffect, QPushButton
from PyQt6.QtCore import pyqtSlot

class BlurButton(QPushButton):
    def __init__(self, text, target_widget, radius: float = 10.0):
        super().__init__(text)

        self.setCheckable(True)
        self.target = target_widget
        self.target_view = target_widget.viewport()
        self.radius = radius

        self.effect = None

        self.toggled.connect(self.on_toggled)

    @pyqtSlot(bool)
    def on_toggled(self, checked):
        if checked:
            self.effect = QGraphicsBlurEffect(self.target_view)
            self.effect.setBlurRadius(self.radius)
            self.target.setGraphicsEffect(self.effect)
        else:
            self.target.setGraphicsEffect(None)
            self.effect = None

        self.target_view.update()
