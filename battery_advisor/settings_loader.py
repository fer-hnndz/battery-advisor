import toml
import os
from .types import Settings
from .utils import _get_project_root

user_settings_path = os.path.expanduser("~/.config/battery-advisor/settings.toml")


def load_settings() -> Settings:
    path = (
        user_settings_path
        if os.path.exists(user_settings_path)
        else _get_project_root() + "/defaultSettings.toml"
    )

    if not os.path.exists(user_settings_path):
        print("User settings not found. Using default settings.")

    with open(path) as f:
        return toml.load(f)
