#!/usr/bin/python3

import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import magic
import toml

from brewDebug import __description__, __version__

from .classes.ctr import CTR
from .classes.hac import HAC
from .config import Config

CONFIG_DIRECTORY = Path().home() / ".config/brewDebug"

FIRST_RUN_PATH = CONFIG_DIRECTORY / ".first_run"
FIRST_RUN_PATH.parent.mkdir(exist_ok=True)

FIRST_RUN_DIALOG = """
This software is not endorsed nor maintained by devkitPro.
If there are issues, please report them to the GitHub repository:
https://github.com/TurtleP/brewDebug
"""

CONFIG = None


def parse_config():
    global CONFIG

    if not (CONFIG_DIRECTORY / "config.toml").exists():
        return False

    try:
        with open(CONFIG_DIRECTORY / "config.toml", "r") as file:
            CONFIG = Config(toml.load(file))
    except Exception as exception:
        print(exception)
        sys.exit(-1)

    return True


def debug_console(file, args):
    if hasattr(args, "elf"):
        if not file or not Path(file).exists():
            return print(f"error: ELF binary does not exist: {file}!")
    else:
        # Check if we are using a specific app from the config
        # return the path based on the console and app
        if hasattr(args, "app"):
            file = CONFIG.get_entry(args.app, args.console)
        else:
            # internally calls get_entry with the first entry
            file = CONFIG.get(args.console)

    filepath = Path(file).expanduser()

    try:
        bin_type = magic.from_file(str(filepath))
        cls_args = [filepath, args]

        HAC(*cls_args) if "aarch64" in bin_type else CTR(*cls_args)
    except Exception as exception:
        print(exception)


def main(args=None):
    if not FIRST_RUN_PATH.exists():
        print(FIRST_RUN_DIALOG)
        FIRST_RUN_PATH.touch()
        return

    if not os.getenv("DEVKITARM") or not os.getenv("DEVKITPRO"):
        return print("critical: devkitPro's software tools not installed. exiting.")

    # get config data if it exists
    parser = ArgumentParser(
        prog="brewDebug", description=__description__, allow_abbrev=True)

    if not parse_config():
        parser.add_argument("elf",     type=str, help="ELF binary")
    else:
        # if a config exists, check if there's more than one entry
        # when there is, add the app argument
        if CONFIG.get_len() > 1:
            parser.add_argument(
                "--app", "-a", type=str, help="app to debug, defaults to the first item in the config", default=CONFIG.get_first())

        parser.add_argument("console", type=str, help="console to debug")

    # REGISTRY GROUP
    reg = parser.add_argument_group("exception registers")

    reg.add_argument("--pc", type=str, help="The Program Counter value",
                     default=None)

    reg.add_argument("--lr", type=str, help="The Link Register value",
                     default=None)

    # LOG
    parser.add_argument("--log", type=str, help="The Log file dump.",
                        default=None)

    # VERSION
    parser.add_argument("--version", "-v", action="version",
                        version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if args.log and (args.pc or args.lr):
        return print("error: cannot use argument 'log' with 'pc' or 'lr'")

    path = None

    if hasattr(args, "elf"):
        path = args.elf
    else:
        path = args.console

    debug_console(path, args)


if __name__ == "__main__":
    main()
