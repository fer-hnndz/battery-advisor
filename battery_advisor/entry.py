from .battery_advisor import BatteryAdvisor, VERSION
import argparse


def cli():
    parser = argparse.ArgumentParser(
        prog="Battery Advisor",
        description="A simple tool to monitor and notify about battery status. Built with Python.",
        epilog="Made with ❤️ by Jorge Hernández.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--clean", action="store_true", help="Use default settings.")

    args = parser.parse_args()
    BatteryAdvisor(clean=args.clean).start()
