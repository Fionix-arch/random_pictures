import sys
from PyQt6.QtWidgets import QToolBar, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 300)

        toolbar = QToolBar("Top", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        bar = QWidget()
        bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        row = QHBoxLayout(bar)
        row.setContentsMargins(0,0,0,0)
        row.setSpacing(0)


        btn_add = QPushButton("+")
        btn_1   = QPushButton("?")
        btn_2   = QPushButton("*") 

        for b in (btn_add, btn_1, btn_2):
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row.addWidget(b, 1)   # одинаковый stretch-фактор

        toolbar.addWidget(bar)
