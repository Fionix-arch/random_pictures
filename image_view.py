from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from pathlib import Path

class ImageViewer(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        pix = QPixmap(str(image_path))

        if not pix.isNull():
            scaled = pix.scaled(
                800, 600,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(scaled)

        self.resize(800, 600)
