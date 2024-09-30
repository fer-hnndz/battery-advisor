import psutil
import subprocess
import os
import time

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


def notify(title: str, message: str):
    """Sends a notification to the user"""
    subprocess.run(["notify-send", title, message, f"--icon={_get_path_icon()}"])


def notify_with_actions(
    title: str,
    message: str,
    options: list[str],
    actions: dict[str, list[str]],
    remind_time: int = 180,
) -> int:
    """Sends a notification with actions to the user"""
    # Send notification command and retrieve selected action

    options_cmd: list[str] = []
    for option in options:
        if option == "remind":
            options_cmd.append(f"--action=Remind in {round(remind_time/60)} mins.")
            continue

        options_cmd.append(f"--action={option.capitalize()}")

    notification_cmd = [
        "notify-send",
        title,
        message,
        f"--icon={_get_path_icon()}",
        f"--expire-time={EXPIRE_TIME}",  # Show notification for 2 minutes
        "--wait",
        "--urgency=critical",
    ]

    #! NOTE: If notification is ignored, the program will hang here.
    #! Hence why notification is shown for 2 minutes.
    notification_cmd.extend(options_cmd)
    command = subprocess.run(
        notification_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    try:
        action_index = int(command.stdout.decode().strip())
    except:
        # User closed the notification
        # Remind the user to charge device
        return remind_time

    selected_action = options[action_index]

    if selected_action == "remind":
        return remind_time

    execute_action(actions[selected_action])
    return 0
