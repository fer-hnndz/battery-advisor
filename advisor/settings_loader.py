import toml
import os
from .types import Settings
from .utils import _get_project_root

user_settings_path = os.path.expanduser("~/.advisor/settings.toml")


def load_settings() -> Settings:
    path = (
        user_settings_path
        if os.path.exists(user_settings_path)
        else _get_project_root() + "/defaultSettings.toml"
    )

    with open(path) as f:
        return toml.load(f)
