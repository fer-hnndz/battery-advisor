import threading
import time

from pystray import Menu, MenuItem
from .settings_loader import Settings
from .tray import get_icon
from .utils import execute_action, get_battery_status
from .notifications import notify, alert_with_options, alert
from .types import BatteryReport
from typing import Optional
from datetime import datetime

VERSION = "1.1.0"


class BatteryAdvisor:
    """Base Program that manages SysTray Icon and the battery checker service."""

    def __init__(self, clean: bool = False):
        """
        Initializes the Battery Advisor program.

        Parameters
        ----------
        clean : bool, optional
            If True, the program will use default settings.
        """
        self.running = True
        self.settings = Settings.load(clean)

    def get_battery_reports(self) -> Optional[BatteryReport]:
        """Returns thet status that needs to be reported to the user"""

        batt_percent, plugged = get_battery_status()

        if plugged:
            return None

        if batt_percent <= self.settings.battery_action_treshold:
            return BatteryReport.ACTION

        if batt_percent <= self.settings.critical_battery_treshold:
            return BatteryReport.CRITICAL

        if batt_percent <= 100:
            return BatteryReport.LOW

        return None

    def _battery_checker(self):
        """
        Service that checks the battery status and notifies the user.
        This one runs in a separate thread because the SysTray icon must run on the main thread.
        """

        print("Starting battery checker...")

        # Always get initial status to avoid false notifications
        _, was_plugged = get_battery_status()
        remind_timestamp = datetime.now()

        while True:
            if not self.running:
                time.sleep(3)
                continue

            print("Checking battery status...")
            _, plugged = get_battery_status()

            # Battery Plugged in notifications
            if plugged != was_plugged:
                was_plugged = plugged
                if plugged and self.settings.notify_plugged:
                    notify("Battery Plugged In", "Battery is now charging")
                elif not plugged and self.settings.notify_unplugged:
                    notify("Battery Unplugged", "Battery is now discharging.")

            report = self.get_battery_reports()
            print("Battery Report:", report)

            if report is None:
                time.sleep(self.settings.check_interval)
                continue

            if report == BatteryReport.ACTION:
                battery_action = self.settings.battery_action
                alert(message=f"Your battery will {battery_action.capitalize()} soon.")
                time.sleep(3)
                execute_action(battery_action, self.settings.actions)

            if report == BatteryReport.CRITICAL:
                alert_with_options(
                    message="Your battery is critically low. Please plug in your charger.",
                    options=self.settings.critical_battery_options,
                    title="Battery Critically Low",
                )

            # Don't sleep for the amount of time to remind the user again.
            # Instead, check if the time has passed using timestamps.

            # This is to avoid excluding critical notifications or if a long remind time is set
            # or plugged/unplugged notifications because of sleep.
            # More like a QoL feature. ;)
            if (
                report == BatteryReport.LOW
                and remind_timestamp.timestamp() <= datetime.now().timestamp()
            ):
                r = alert_with_options(
                    "Battery is low. Please plug in your charger.",
                    self.settings.low_battery_options,
                    title="Battery Low",
                )

                selected_action = self.settings.low_battery_options[r]

                if selected_action == "remind":
                    remind_timestamp = datetime.fromtimestamp(
                        remind_timestamp.timestamp() + self.settings.remind_time
                    )

                else:
                    execute_action(selected_action, self.settings.actions)

            time.sleep(self.settings.check_interval)

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
            ),
            MenuItem(text=f"Version: {VERSION}", checked=None, action=None),
        )
        get_icon(menu).run()
        print("Exiting...")
        return 0
