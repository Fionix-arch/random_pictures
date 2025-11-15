import sys
import random
from PyQt6.QtWidgets import QToolBar, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QListView
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from pathlib import Path

from buttoms.add_buttom import FolderButton
from buttoms.blur_buttom import BlurButton

class MainWindow(QMainWindow):
    def __init__(self, path: Path):
        super().__init__()

        self.path = path

        self.resize(500, 300)

        toolbar = QToolBar("Top", self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        bar = QWidget()
        bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        row = QHBoxLayout(bar)
        row.setContentsMargins(0,0,0,0)
        row.setSpacing(0)

        self.grid = QListWidget()
        self.grid.setViewMode(QListView.ViewMode.IconMode)
        self.grid.setIconSize(QSize(160, 160))
        self.grid.setResizeMode(QListView.ResizeMode.Adjust)
        self.grid.setSpacing(8)
        self.grid.setUniformItemSizes(True)
        self.grid.setWordWrap(True)
        self.setCentralWidget(self.grid)


        btn_add = FolderButton("+", self.path, self.load_images)
        btn_shuffle   = QPushButton("?")
        btn_shuffle.clicked.connect(self.shuffle_image)
        btn_blur   = BlurButton("*", self.grid, 50.0) 

        for b in (btn_add, btn_shuffle, btn_blur):
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row.addWidget(b, 1)   

        toolbar.addWidget(bar)
 
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

    def shuffle_image(self):
        item = []

        while self.grid.count() > 0:
            item.append(self.grid.takeItem(0))

        random.shuffle(item)

        for it in item:
            self.grid.addItem(it)


