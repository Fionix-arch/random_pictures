from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl, QFileSystemWatcher

class FolderButton(QPushButton):
    def __init__(self, text, folder_path, on_refresh):
        super().__init__(text)
        self.folder_path = folder_path      
        self.on_refresh = on_refresh        
        self.clicked.connect(self.open_folder)

        self.watcher = QFileSystemWatcher([str(self.folder_path)])
        self.watcher.directoryChanged.connect(self.on_refresh)

    def open_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.folder_path)))

