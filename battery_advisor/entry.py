from .battery_advisor import BatteryAdvisor, VERSION
import argparse
import logging
import os
from .utils import get_log_path
import traceback


def cli():
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s ] (%(module)s.%(funcName)s | %(levelname)s) %(message)s",
            datefmt="%d/%m/%Y @ %H:%M:%S %Z",
            filename=get_log_path(),
        )

        parser = argparse.ArgumentParser(
            prog="Battery Advisor",
            description="A simple tool to monitor and notify about battery status. Built with Python.",
            epilog="Made with ❤️ by Jorge Hernández.",
        )
        parser.add_argument(
            "--version", action="version", version=f"%(prog)s {VERSION}"
        )
        parser.add_argument(
            "--clean", action="store_true", help="Use default settings."
        )

        args = parser.parse_args()
        BatteryAdvisor(clean=args.clean).start()
    except Exception as e:
        logging.error(traceback.format_exc())
        quit(1)
