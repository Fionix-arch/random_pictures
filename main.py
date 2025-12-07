import os
import sys
import platform
if platform.system == "Linux" and os.envirop.get("WAYLAND_DISPLAY"):
    os.envirop.setdefault("QT_QPA_PLATFORM", "wayland")
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from pywal_them import apply_pywal_to_app

def dir_pictures():
    app_dir = Path.home() / ".dir_pictures"
    app_dir.mkdir(parents = True, exist_ok = True)
    return app_dir

if __name__ == "__main__":
    dir_pictures()

    app = QApplication(sys.argv)
    apply_pywal_to_app(app)
    window = MainWindow(dir_pictures())
    window.show()
    sys.exit(app.exec())
