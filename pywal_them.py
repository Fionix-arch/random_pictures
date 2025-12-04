from pathlib import Path
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor

def load_pywal_palette():
    wal_json = Path.home() / ".cache" / "wal" / "colors.json"
    if not wal_json.exists():
        return None

    with wal_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data  

def apply_pywal_to_app(app: QApplication):
    data = load_pywal_palette()
    if data is None:
        return

    bg_hex = data["special"]["background"]
    fg_hex = data["special"]["foreground"]
    accent_hex = data["colors"].get("color4", fg_hex)  

    bg = QColor(bg_hex)
    fg = QColor(fg_hex)
    accent = QColor(accent_hex)

    palette = app.palette()

    palette.setColor(QPalette.ColorRole.Window, bg)
    palette.setColor(QPalette.ColorRole.WindowText, fg)

    palette.setColor(QPalette.ColorRole.Base, bg.darker(115))
    palette.setColor(QPalette.ColorRole.Text, fg)

    palette.setColor(QPalette.ColorRole.Button, bg.darker(110))
    palette.setColor(QPalette.ColorRole.ButtonText, fg)

    palette.setColor(QPalette.ColorRole.Highlight, accent)
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))

    app.setPalette(palette)
