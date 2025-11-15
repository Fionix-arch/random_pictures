import sys
import random
from PyQt6.QtWidgets import QToolBar, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QListView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QImage
from pathlib import Path

from image_view import ImageViewer
from buttoms.add_buttom import FolderButton
from buttoms.blur_buttom import BlurButton
from buttoms.random_pictures_buttom import RandomImageButton

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
        self.grid.itemActivated.connect(self.open_image_from_item)
        self.setCentralWidget(self.grid)


        btn_add = FolderButton("+", self.path, self.load_images)
        btn_shuffle   = QPushButton("?")
        btn_shuffle.clicked.connect(self.shuffle_image)
        btn_blur   = BlurButton("*", self.set_blur_enabled ) 
        btn_random = RandomImageButton("#", self.open_random_image)

        for b in (btn_add, btn_shuffle, btn_blur, btn_random):
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

                    blur_thumb = self.blur_pixmap(thumb, 25.0)
                    item = QListWidgetItem(QIcon(thumb), path.stem)
                    item.setToolTip(str(path))

                    item.setData(Qt.ItemDataRole.UserRole, thumb)
                    item.setData(Qt.ItemDataRole.UserRole + 1, blur_thumb)
                    self.grid.addItem(item)

    def shuffle_image(self):
        item = []

        while self.grid.count() > 0:
            item.append(self.grid.takeItem(0))

        random.shuffle(item)

        for it in item:
            self.grid.addItem(it)

    def blur_pixmap(self, pixmap: QPixmap, radius):
        if pixmap.isNull():
            return pixmap
        
        self.img = QImage(pixmap.size(), QImage.Format.Format_ARGB32)
        self.img.fill(Qt.GlobalColor.transparent)

        self.scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem(pixmap)
        self.blur = QGraphicsBlurEffect()
        self.blur.setBlurRadius(radius)
        self.item.setGraphicsEffect(self.blur)
        self.scene.addItem(self.item)

        self.painter = QPainter(self.img)
        self.scene.render(self.painter)
        self.painter.end()

        return QPixmap.fromImage(self.img)

    def set_blur_enabled(self, enabled):
        for i in range(self.grid.count()):
            item = self.grid.item(i)
            normal_pix = item.data(Qt.ItemDataRole.UserRole)
            blur_pix = item.data(Qt.ItemDataRole.UserRole + 1)

            if enabled:
                icon_pix = blur_pix
            else:
                icon_pix = normal_pix

            item.setIcon(QIcon(icon_pix))

    def open_image_from_item(self, item):
        path = Path(item.toolTip())
        if not path.exists():
            return
        viewer = ImageViewer(path, self)
        viewer.exec()

    def open_random_image(self):
        count = self.grid.count()
        if count == 0:
            return
        
        index = random.randrange(count)
        item = self.grid.item(index)
        self.open_image_from_item(item)
