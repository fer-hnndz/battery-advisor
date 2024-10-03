import os
import subprocess

import psutil

EXPIRE_TIME = 600000  # 10 minutes


def _get_project_root() -> str:
    usr_home = os.path.expanduser("~")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_root = root.replace(usr_home, "$HOME")
    return os.path.expandvars(absolute_root)


def get_log_path() -> str:
    return os.path.expanduser("~/.battery-advisor.log")


def _get_path_icon():
    icon_path = _get_project_root() + "/icon.png"
    return os.path.expandvars(icon_path)


def get_battery_status() -> tuple[int, bool]:
    """Returns the battery percentage and if it is plugged in"""
    batt = psutil.sensors_battery()
    return batt.percent, batt.power_plugged


def execute_action(action_name: str, actions: dict[str, list[str]]) -> None:
    """Executes specified action

    Parameters
    ----------
    action : list[str]
        The name of the action to execute
    """

    try:
        subprocess.run(actions[action_name], stdout=subprocess.PIPE)
    except Exception as e:
        print("Failed to perform action: ", e)
