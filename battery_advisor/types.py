from typing import Literal, TypedDict
from enum import Enum


class Tresholds(TypedDict):
    low_battery_treshold: int
    critical_battery_treshold: int
    battery_action_treshold: int


class Advisor(TypedDict):
    notify_plugged: bool
    notify_unplugged: bool
    battery_action: str
    low_battery_options: list[str]
    critical_battery_options: list[str]
    remind_time: int
    check_interval: int


class SettingsFile(TypedDict):
    tresholds: Tresholds
    advisor: Advisor
    actions: dict[str, list[str]]


class BatteryReport(Enum):
    LOW = 0
    CRITICAL = 1
    ACTION = 2
