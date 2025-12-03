import sys
import json
import os
import random
from PyQt6.QtWidgets import QToolBar, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QListView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsBlurEffect, QInputDialog
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QImage
from pathlib import Path

from set_wallpaper import SetWallpaper
from image_view import ImageViewer
from buttoms.add_buttom import FolderButton
from buttoms.blur_buttom import BlurButton
from buttoms.random_pictures_buttom import RandomImageButton
from buttoms.wallpaper_cycle import WallpaperCycler

class MainWindow(QMainWindow):
    def __init__(self, path: Path):
        super().__init__()

        self.path = path
        self.cache_dir = self.path / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_index_path = self.cache_dir / "thumb.json"
        self.cache_index = self.load_cache_index()

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
        self.grid.itemActivated.connect(self.set_wallpaper_from_item)
        self.setCentralWidget(self.grid)

        self.cycler = WallpaperCycler(self.grid, self)

        btn_add = FolderButton("+", self.path, self.load_images)
        btn_shuffle   = QPushButton("?")
        btn_shuffle.clicked.connect(self.shuffle_image)
        btn_random = RandomImageButton("#", self.open_random_image)
        btn_cycle = QPushButton("⟳")
        btn_cycle.setCheckable(True)
        btn_cycle.toggled.connect(self.on_cycle_toggled)

        for b in (btn_add, btn_shuffle, btn_random, btn_cycle):
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row.addWidget(b, 1)   

        toolbar.addWidget(bar)
 
        self.items_by_path: dict[str, QListWidgetItem] = {}
        self.load_images()

    def on_cycle_toggled(self, checked):
        if checked:
            seconds, ok = QInputDialog.getInt(
                self,
                "Интервал смены обоев",
            "Каждые сколько секунд менять обои?",
            value=10,
            min=1,
            max=3600,

            )
            if not ok:
                sender = self.sender()
                if sender is not None:
                    sender.setChecked(False)
                return
            self.cycler.start(seconds)

        else:
            self.cycler.stop()

    def set_wallpaper_from_item(self, item: QListWidgetItem):
        path = Path(item.toolTip())  
        SetWallpaper.set_wallpaper(path)

    def load_cache_index(self):
        if not self.cache_index_path.exists():
            return {}
        try:
            with self.cache_index_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_cache_index(self):
        with self.cache_index_path.open("w", encoding="utf-8") as f:
            json.dump(self.cache_index, f, ensure_ascii=False, indent=2)

    def get_thumb_with_cache(self, path: Path) -> QPixmap | None:
        key = str(path)
        stat = path.stat()
        mtime = stat.st_mtime
        size = stat.st_size

        entry = self.cache_index.get(key)

        if entry:
            if entry.get("mtime") == mtime and entry.get("size") == size:
                thumb_path = Path(entry["thumb"])
                if thumb_path.exists():
                    pix = QPixmap(str(thumb_path))
                    if not pix.isNull():
                        return pix 

        pix = QPixmap(str(path))
        if pix.isNull():
            return None

        thumb = pix.scaled(
        self.grid.iconSize(),
        aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
        transformMode=Qt.TransformationMode.FastTransformation,  
    )

        thumb_name = f"{hash(key)}.png"  
        thumb_path = self.cache_dir / thumb_name
        thumb.save(str(thumb_path), "PNG")

        self.cache_index[key] = {
        "mtime": mtime,
        "size": size,
        "thumb": str(thumb_path),
    }

        return thumb

    def load_images(self):

        exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}

        files = [p for p in self.path.iterdir() if p.is_file() and p.suffix.lower() in exts]
        files_set = {str(p) for p in files}
        existing_set = set(self.items_by_path.keys())

        for lost in existing_set - files_set:
            item = self.items_by_path.pop(lost)
            row = self.grid.row(item)
            self.grid.takeItem(row)


        for path in sorted(files):
            key = str(path)
            
            if key in self.items_by_path:
                continue

            thumb = self.get_thumb_with_cache(path)
            if thumb is None:
                continue
            item = QListWidgetItem(QIcon(thumb), path.stem)
            item.setToolTip(str(path))

            item.setData(Qt.ItemDataRole.UserRole, thumb)
            self.grid.addItem(item)
            self.items_by_path[key] = item
        self.save_cache_index()

    def shuffle_image(self):
        item = []

        while self.grid.count() > 0:
            item.append(self.grid.takeItem(0))

        random.shuffle(item)

        for it in item:
            self.grid.addItem(it)

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
