import os
import subprocess

import psutil

EXPIRE_TIME = 600000  # 10 minutes


def _get_project_root() -> str:
    usr_home = os.path.expanduser("~")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_root = root.replace(usr_home, "$HOME")
    return os.path.expandvars(absolute_root)


def _get_path_icon():
    icon_path = _get_project_root() + "/icon.png"
    return os.path.expandvars(icon_path)


def get_battery_status() -> tuple[int, bool]:
    """Returns the battery percentage and if it is plugged in"""
    batt = psutil.sensors_battery()
    return batt.percent, batt.power_plugged


def execute_action(action: list[str]) -> None:
    """Executes specified action

    Parameters
    ----------
    action : list[str]
        List of strings that make up the command to be executed.
    """

    try:
        a = subprocess.run(action)
    except Exception as e:
        notify(
            "Error",
            f"Failed to perform action. Perhaps the actions is not valid.\n\n{e}",
        )
