import subprocess

from .utils import _get_path_icon, execute_action
from .gui.alerts import AlertWithButtons, MessageAlert

EXPIRE_TIME = 160000


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


def alert(message: str):
    """Sends a popup to the user"""
    dialog = MessageAlert(message=message)
    dialog.run()
    dialog.destroy()


def alert_with_options(message: str, options: list[str]) -> int:
    """Sends a popup with a close option to the user.

    Returns
    -------
    int
        The selected option index
    """

    dialog = AlertWithButtons(message=message, actions=options)
    selection = dialog.run()
    dialog.destroy()
    return selection
