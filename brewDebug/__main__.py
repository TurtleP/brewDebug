#!/usr/bin/python3

import os
from argparse import ArgumentParser
from pathlib import Path

import magic

from brewDebug import __description__, __version__

from .classes.ctr import CTR
from .classes.hac import HAC

FIRST_RUN_PATH = Path().home() / ".config/brewDebug/.first_run"
FIRST_RUN_PATH.parent.mkdir(exist_ok=True)

FIRST_RUN_DIALOG = """
This software is not endorsed nor maintained by devkitPro.
If there are issues, please report them to the GitHub repository:
https://github.com/TurtleP/brewDebug
"""

def debug_console(file, args):
    if not file:
        return print(f"ELF binary does not exist: {file}!")

    bin_type = magic.from_file(file)

    HAC(args) if "aarch64" in bin_type else CTR(args)


def main(args=None):
    if not FIRST_RUN_PATH.exists():
        print(FIRST_RUN_DIALOG)
        FIRST_RUN_PATH.touch()
        return

    if not os.getenv("DEVKITARM") or not os.getenv("DEVKITPRO"):
        return print("critical: devkitPro's software tools not installed. exiting.")

    parser = ArgumentParser(prog="brewDebug", description=__description__)

    parser.add_argument("elf", type=str, help="ELF binary")

    parser.add_argument("--pc", type=str, help="The Program Counter value",
                        default=None)

    parser.add_argument("--lr", type=str, help="The Link Register value",
                        default=None)

    parser.add_argument("--log", type=str, help="The Log file dump.",
                        default=None)

    parser.add_argument("--version", "-v", action="version",
                        version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if args.log and (args.pc or args.lr):
        return print("error: cannot use argument 'log' with 'pc' or 'lr'")

    debug_console(args.elf, args)


if __name__ == "__main__":
    main()
