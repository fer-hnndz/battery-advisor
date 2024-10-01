import pystray
from PIL import Image
from PIL.ImageFile import ImageFile
from .utils import _get_project_root


def _get_icon_from_image(image_path: str) -> ImageFile:
    """Returns an image object from a file path"""
    return Image.open(image_path)


def get_icon(menu: pystray.Menu):
    icon_path = _get_project_root() + "/icon.png"
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
