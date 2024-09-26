import psutil
import subprocess
import os


def _get_project_root() -> str:
    usr_home = os.path.expanduser("~")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_root = root.replace(usr_home, "$HOME")
    return os.path.expandvars(absolute_root)


def _get_path_icon():
    icon_path = _get_project_root() + "/icon.png"
    return os.path.expandvars(icon_path)


def get_battery_status():
    batt = psutil.sensors_battery()
    return batt.percent, batt.power_plugged


def notify(title: str, message: str):
    subprocess.run(["notify-send", title, message, f"--icon={_get_path_icon()}"])
