import pystray
from PIL import Image, ImageDraw
from PIL.ImageFile import ImageFile
from .utils import _get_project_root
from typing import Generator

MENU_APP_ENABLED = True


def _get_icon_from_image(image_path: str) -> ImageFile:
    """Returns an image object from a file path"""
    return Image.open(image_path)


def on_enabled_click(icon, item):
    global MENU_APP_ENABLED
    MENU_APP_ENABLED = not MENU_APP_ENABLED


def get_icon():
    icon_path = _get_project_root() + "/icon.png"
    menu = pystray.Menu(
        pystray.MenuItem(
            text="Enabled",
            checked=lambda item: MENU_APP_ENABLED,
            action=on_enabled_click,
        ),
        pystray.MenuItem("Item 2", lambda: print("Item 2")),
    )

    i = pystray.Icon(
        name="Battery Advisor",
        icon=_get_icon_from_image(icon_path),
        title="Battery Advisor",
        menu=menu,
    )

    if not i.HAS_MENU:
        # Warn no menu
        print("No menu available for this platform.")

    return i
