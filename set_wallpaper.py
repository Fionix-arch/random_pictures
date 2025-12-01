# set_wallpaper.py
import os
import platform
import subprocess
import ctypes
import shutil
from pathlib import Path


class SetWallpaper:
    @staticmethod
    def set_wallpaper_windows(path: Path) -> bool:
        SPI_SETDESKWALLPAPER = 20
        try:
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, str(path), 3
            )
            return True
        except Exception:
            return False

    @staticmethod
    def set_wallpaper_gnome(path: Path) -> bool:
        uri = f"file://{path.absolute()}"

        cmds = [
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri],
        ]

        ok = False
        for cmd in cmds:
            try:
                subprocess.run(cmd, check=True)
                ok = True
            except subprocess.CalledProcessError:
                pass

        return ok

    @staticmethod
    def set_wallpaper_hypr_swww(path: Path) -> bool:
        if shutil.which("swww") is None:
            return False

        try:
            subprocess.run(["swww", "img", str(path)], check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def set_wallpaper(path: Path) -> bool:
        path = path.absolute()
        system = platform.system()

        if system == "Windows":
            return SetWallpaper.set_wallpaper_windows(path)

        if system == "Linux":
            if os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
                if SetWallpaper.set_wallpaper_hypr_swww(path):
                    return True

            desktop = (os.environ.get("XDG_CURRENT_DESKTOP") or "").lower()
            if any(x in desktop for x in ("gnome", "cinnamon", "mate", "unity")):
                return SetWallpaper.set_wallpaper_gnome(path)

        return False
 
