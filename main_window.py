import sys
from PyQt6.QtWidgets import QToolBar, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QListView
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self, path: Path):
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
            row.addWidget(b, 1)   

        toolbar.addWidget(bar)

        self.path = path

        self.grid = QListWidget()
        self.grid.setViewMode(QListView.ViewMode.IconMode)
        self.grid.setIconSize(QSize(160, 160))
        self.grid.setResizeMode(QListView.ResizeMode.Adjust)
        self.grid.setSpacing(8)
        self.grid.setUniformItemSizes(True)
        self.grid.setWordWrap(True)
        self.setCentralWidget(self.grid)

        self.load_images()


    def load_images(self):

        exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}

        self.grid.clear()  

        for path in sorted(self.path.iterdir()):
            if path.is_file() and path.suffix.lower() in exts:
                pix = QPixmap(str(path))
                if not pix.isNull():
                    thumb = pix.scaled(
                        self.grid.iconSize(),
                        aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                        transformMode=Qt.TransformationMode.SmoothTransformation
                    )
                    item = QListWidgetItem(QIcon(thumb), path.stem)
                    item.setToolTip(str(path))
                    self.grid.addItem(item)


