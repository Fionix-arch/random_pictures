from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QListWidget
from pathlib import Path

import sys
sys.path.append('../')
from set_wallpaper import SetWallpaper

class WallpaperCycler(QObject):
    def __init__(self, grid, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_tick)
        self.index = 0

    def start(self, interval):
        count = self.grid.count()
        if count == 0:
            return 

        self.index = 0
        interval_ms =  max(1, int(interval * 1000))
        self.timer.start(interval_ms)

    def stop(self):
        self.timer.stop()

    def is_running(self):
        return self.timer.isActive()

    def on_tick(self):
        count = self.grid.count()
        if count == 0:
            self.stop()
            return

        if self.index >= count:
            self.index = 0

        item = self.grid.item(self.index)
        path = Path(item.toolTip())
        SetWallpaper.set_wallpaper(path)

        self.index +=1
