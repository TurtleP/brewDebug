from argparse import ArgumentParser

import magic
from brewDebug import __description__, __version__


def get_console(file, args):
    bin_type = magic.from_file(file)

    return bin_type


def main(args=None):
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
        return print("error: cannot use 'log' with 'pc' or 'lr'")

    get_console(args.elf, args)


if __name__ == "__main__":
    main()
