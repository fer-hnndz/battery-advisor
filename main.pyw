import time
from advisor import get_battery_status, notify, load_settings, notify_with_actions

settings = load_settings()

# LOW_BATTERY_TRESHOLD = settings["tresholds"]["low_battery_treshold"]
LOW_BATTERY_TRESHOLD = 90
CRITICAL_BATTERY_TRESHOLD = settings["tresholds"]["critical_battery_treshold"]
BATTERY_ACTION_TRESHOLD = settings["tresholds"]["battery_action_treshold"]
CHECK_INTERVAL = settings["advisor"]["check_interval"]

# Configs
NOTIFY_PLUGGED = settings["advisor"]["notify_plugged"]
NOTIFY_UNPLUGGED = settings["advisor"]["notify_unplugged"]

# Actions
LOW_BATTERY_OPTIONS = settings["advisor"]["low_battery_options"]
CRITICAL_BATTERY_OPTIONS = settings["advisor"]["critical_battery_options"]

if __name__ == "__main__":
    _, was_plugged = get_battery_status()

    while True:
        remind_time = 0
        batt_percent, plugged = get_battery_status()

        # Battery Plugged in notifications
        if plugged != was_plugged:
            was_plugged = plugged
            if plugged and NOTIFY_PLUGGED:
                notify("Battery Plugged In", "Battery is now charging")
            elif not plugged and NOTIFY_UNPLUGGED:
                notify("Battery Unplugged", "Battery is now discharging.")

        # Battery Low notifications
        if batt_percent <= LOW_BATTERY_TRESHOLD:
            remind_time = notify_with_actions(
                title="Low Battery",
                message=f"Consider plugging your device.",
                options=LOW_BATTERY_OPTIONS,
                actions=settings["actions"],
                remind_time=settings["advisor"]["remind_time"],
            )

        if remind_time > 0:
            print("A function returned a remind time!")
            time.sleep(remind_time)
            continue

        time.sleep(CHECK_INTERVAL)
