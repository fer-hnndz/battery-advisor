import time
from advisor import get_battery_status, notify, load_settings

BATTERY_TRESHOLD = 15


if __name__ == "__main__":
    settings = load_settings()
    p, was_plugged = get_battery_status()

    notify("Battery Advisor", "Battery Advisor is now running...")
    while True:

        batt_percent, plugged = get_battery_status()

        # Battery Plugged in notifications
        if plugged != was_plugged:
            if plugged:
                notify("Battery Plugged In", "Battery is now charging")
            else:
                notify("Battery Unplugged", "Battery is now discharging")

        time.sleep(settings["advisor"]["check_every"])
