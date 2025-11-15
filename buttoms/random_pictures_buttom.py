from PyQt6.QtWidgets import QPushButton

class RandomImageButton(QPushButton):
    def __init__(self, text, on_click):
        super().__init__(text)
        self.clicked.connect(on_click)
