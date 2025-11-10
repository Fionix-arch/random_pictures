import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def dir_pictures():
    app_dir = Path.home() / ".dir_pictures"
    app_dir.mkdir(parents = True, exist_ok = True)
    return app_dir

if __name__ == "__main__":
    dir_pictures()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
