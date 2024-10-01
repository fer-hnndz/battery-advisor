import time
from .utils import get_battery_status, notify, notify_with_actions, execute_action
from .settings_loader import load_settings
from .gui.alerts import MessageAlert, AlertWithButtons
from .tray import get_icon

import threading
from pystray import Menu, MenuItem

settings = load_settings()


class BatteryAdvisor:
    LOW_BATTERY_TRESHOLD = settings["tresholds"]["low_battery_treshold"]
    CRITICAL_BATTERY_TRESHOLD = settings["tresholds"]["critical_battery_treshold"]
    BATTERY_ACTION_TRESHOLD = settings["tresholds"]["battery_action_treshold"]
    CHECK_INTERVAL = settings["advisor"]["check_interval"]

    # Configs
    NOTIFY_PLUGGED = settings["advisor"]["notify_plugged"]
    NOTIFY_UNPLUGGED = settings["advisor"]["notify_unplugged"]

    # Actions
    LOW_BATTERY_OPTIONS = settings["advisor"]["low_battery_options"]
    CRITICAL_BATTERY_OPTIONS = settings["advisor"]["critical_battery_options"]

    def __init__(self):
        self.running = True

    def _battery_checker(self):
        print("Starting battery checker...")
        _, was_plugged = get_battery_status()

        while True:
            if not self.running:
                time.sleep(1)
                continue

            print("Checking battery status...")
            remind_time = 0
            batt_percent, plugged = get_battery_status()

            # Battery Plugged in notifications
            if plugged != was_plugged:
                was_plugged = plugged
                if plugged and self.NOTIFY_PLUGGED:
                    notify("Battery Plugged In", "Battery is now charging")
                elif not plugged and self.NOTIFY_UNPLUGGED:
                    notify("Battery Unplugged", "Battery is now discharging.")

            if plugged:
                print("Battery is charging. Skipping checks.")
                print("Sleeping...")
                time.sleep(self.CHECK_INTERVAL)
                continue

            # Battery Low notifications
            if batt_percent <= self.BATTERY_ACTION_TRESHOLD:
                notify(
                    "Battery Action",
                    f"Your battery is at {batt_percent}%. Your system will {settings['advisor']['battery_action'].capitalize()} in a few.",
                )
                print("Reporting battery action.")
                print("Sleeping...")
                time.sleep(5)
                configured_action = settings["advisor"]["battery_action"]
                action_cmd = settings["actions"][configured_action]
                print("Executing Battery Action. Goodbye...")
                execute_action(action_cmd)

            if batt_percent <= self.CRITICAL_BATTERY_TRESHOLD:
                print("Reporting critical battery.")
                remind_time = notify_with_actions(
                    title="CRITICAL BATTERY",
                    message=f"Your battery is at {int(batt_percent)}%. Consider plugging your device.",
                    options=self.CRITICAL_BATTERY_OPTIONS,
                    actions=settings["actions"],
                    remind_time=round(
                        settings["advisor"]["remind_time"] / 2
                    ),  # Remind in half the remind time
                )

            elif batt_percent <= self.LOW_BATTERY_TRESHOLD:
                print("Reporting low battery.")
                remind_time = notify_with_actions(
                    title="Low Battery",
                    message=f"Consider plugging your device.",
                    options=self.LOW_BATTERY_OPTIONS,
                    actions=settings["actions"],
                    remind_time=settings["advisor"]["remind_time"],
                )

            if remind_time > 0:
                print("A function returned a remind time!")
                time.sleep(remind_time)
                continue

            print("Sleeping...")
            time.sleep(self.CHECK_INTERVAL)

    def _on_enabled_click(self, icon, item):
        self.running = not self.running
        print("Battery Advisor is now", "enabled" if self.running else "disabled")

    def start(self):
        batt_thread = threading.Thread(target=self._battery_checker, daemon=True)
        batt_thread.start()

        menu = Menu(
            MenuItem(
                text="Enabled",
                checked=lambda item: self.running,
                action=self._on_enabled_click,
            )
        )
        get_icon(menu).run()
        print("Exiting...")
        return 0
