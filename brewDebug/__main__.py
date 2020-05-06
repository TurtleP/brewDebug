__author__ = "TurtleP"
__copyright__ = f"Copyright (c) 2020 {__author__}"
__license__ = "MIT"
__version__ = "0.1.0"


import argparse

import magic

from .data.n3ds import N3DS
from .data.switch import Switch


def get_console(file, args):
    data = magic.from_file(file)
    tmp_cls = N3DS

    if "aarch64" in data:
        tmp_cls = Switch

    return tmp_cls(args.elf, pc=args.pc, lr=args.lr, log_path=args.log)


def main(args=None):
    DESCRIPTION = "Debugging utility for libctru and libnx homebrew ELF " \
                  "binaries."

    parser = argparse.ArgumentParser(prog="brewDebug",
                                     description=DESCRIPTION)

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

    # get the console we want and debug it
    get_console(args.elf, args).run_debug()


if __name__ == "__main__":
    main()
