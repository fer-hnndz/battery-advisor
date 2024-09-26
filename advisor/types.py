from typing import TypedDict, Literal


class Tresholds(TypedDict):
    low_battery_treshold: int
    critical_battery_treshold: int
    battery_action_treshold: int


class Advisor(TypedDict):
    notify_plugged: bool
    notify_unplugged: bool
    battery_action: str
    low_battery_options: tuple[str]
    critical_battery_options: tuple[str]
    remind_time: int
    check_every: int


class Settings(TypedDict):
    tresholds: Tresholds
    advisor: Advisor
    actions: dict[str, str]
