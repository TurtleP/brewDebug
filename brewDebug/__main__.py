#!/usr/bin/python3

import os
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

    with open(CONFIG_DIRECTORY / "config.toml", "r") as file:
        CONFIG = Config(toml.load(file))

    return True


def debug_console(file, args):
    path = file

    if Path(file).suffix == ".elf":
        if not file or not Path(file).exists():
            return print(f"error: ELF binary does not exist: {file}!")
    else:
        path = CONFIG.get(file)

    try:
        bin_type = magic.from_file(path)

        HAC(args) if "aarch64" in bin_type else CTR(args)
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
    parser = ArgumentParser(prog="brewDebug", description=__description__)

    if not parse_config():
        parser.add_argument("elf",     type=str, help="ELF binary")
    else:
        parser.add_argument("console", type=str, help="console to debug")

    # REGISTRY GROUP

    reg = parser.add_argument_group("exception registers")

    reg.add_argument("--pc", type=str, help="The Program Counter value",
                     default=None)

    reg.add_argument("--lr", type=str, help="The Link Register value",
                     default=None)

    # LOG GROUP
    parser.add_argument("--log", type=str, help="The Log file dump.",
                        default=None)

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
