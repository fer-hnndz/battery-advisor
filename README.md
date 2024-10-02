# battery-advisor

A simple tool to monitor and notify about battery status. Built with Python.

**Features**
- A system tray icon to enable/disable monitoring
- Notifications for charging status
- Popups for low battery status
- Highly configurable notification for battery levels.

## Installation
The program can be installed from the AUR.
I suggest to use an AUR helper, like `yay`.

```bash
$ yay -S battery-advisor
```

# Dependencies 
- libnotify
- python-gobject
- python-pystray
- python-toml
- python-psutil
