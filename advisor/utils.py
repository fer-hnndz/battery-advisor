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


def get_battery_status() -> tuple[int, bool]:
    """Returns the battery percentage and if it is plugged in"""
    batt = psutil.sensors_battery()
    return batt.percent, batt.power_plugged


def notify(title: str, message: str):
    """Sends a notification to the user"""
    subprocess.run(["notify-send", title, message, f"--icon={_get_path_icon()}"])


def notify_with_actions(
    title: str, message: str, options: list[str], actions: dict[str, str]
):
    """Sends a notification with actions to the user"""
    # Send notification command and retrieve selected action

    options_cmd = [f"--action={action.capitalize()}" for action in options]
    notification_cmd = [
        "notify-send",
        title,
        message,
        f"--icon={_get_path_icon()}",
        "--wait",
    ]
    notification_cmd.extend(options_cmd)
    command = subprocess.run(
        notification_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    try:
        action_index = int(command.stdout.decode().strip())
    except:
        return

    selected_action = options[action_index]

    # Perform action
    try:
        a = subprocess.run(actions[selected_action])
    except Exception as e:
        notify(
            "Error",
            f"Failed to perform action. Perhaps the actions is not valid.\n\n{e}",
        )
        return
