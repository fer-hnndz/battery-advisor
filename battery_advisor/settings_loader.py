import os
import toml
from typing import Type
from .types import SettingsFile
from .utils import _get_project_root
import logging


logger = logging.getLogger(__name__)
user_settings_path = os.path.expanduser("~/.config/battery-advisor/settings.toml")
default_settings_path = _get_project_root() + "/defaultSettings.toml"


def load_settings(load_default: bool = False) -> SettingsFile:
    """Loads the settings from the settings.toml file and returns a dictionary with the settings

    Parameters
    ----------
    load_default : bool, optional
        If True, the default settings will be loaded instead of the user settings.
    """

    if load_default:
        logging.info("(--clean) Loading default settings...")
        with open(default_settings_path) as f:
            return toml.load(f)

    path = (
        user_settings_path
        if os.path.exists(user_settings_path)
        else default_settings_path
    )

    if not os.path.exists(user_settings_path):
        logging.warning("User settings not found. Using default settings.")

    with open(path) as f:
        return toml.load(f)


class Settings:
    def __init__(self, settings: SettingsFile):
        """Creates a settings object based on the settings.toml file.
        NOTE: This class is not meant to be instantiated directly. Use the load() method instead.
        """

        self.check_interval: int = int(settings["advisor"]["check_interval"])
        self.remind_time: int = int(settings["advisor"]["remind_time"])

        # Tresholds
        self.low_battery_treshold = settings["tresholds"]["low_battery_treshold"]
        self.critical_battery_treshold = settings["tresholds"][
            "critical_battery_treshold"
        ]
        self.battery_action_treshold = settings["tresholds"]["battery_action_treshold"]

        # Alert Options
        self.low_battery_options = settings["advisor"]["low_battery_options"]
        self.critical_battery_options = settings["advisor"]["critical_battery_options"]
        self.battery_action = settings["advisor"]["battery_action"]

        self.actions: dict[str, list[str]] = settings["actions"]

        # Notification Settings
        self.notify_plugged = settings["advisor"]["notify_plugged"]
        self.notify_unplugged = settings["advisor"]["notify_unplugged"]

    @classmethod
    def load(cls: Type["Settings"], clean: bool = False) -> "Settings":
        """Loads the settings from the settings.toml file and returns a Settings object

        Parameters
        ----------
        clean : bool, optional
            If True, the default settings will be loaded instead of the user settings.
        """

        return cls(load_settings(load_default=clean))
