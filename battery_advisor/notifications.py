import subprocess

from .utils import _get_path_icon, execute_action
from .gui.alerts import AlertWithButtons, MessageAlert

EXPIRE_TIME = 160000


def notify(title: str, message: str):
    """Sends a notification to the user"""
    subprocess.run(["notify-send", title, message, f"--icon={_get_path_icon()}"])


def alert(message: str, title: str = "Battery Advisor"):
    """Sends a popup to the user"""
    dialog = MessageAlert(message=message, title=title)
    dialog.run()
    dialog.destroy()


def alert_with_options(
    message: str, options: list[str], title: str = "Battery Advisor"
) -> int:
    """Sends a popup with a close option to the user.

    Returns
    -------
    int
        The selected option index
    """

    dialog = AlertWithButtons(title=title, message=message, actions=options)
    selection = dialog.run()
    dialog.destroy()
    return selection
