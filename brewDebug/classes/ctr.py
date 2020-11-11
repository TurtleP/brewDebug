import os
import subprocess
from pathlib import Path

from .console import Console


class CTR(Console):

    def __init__(self, args):
        super().__init__(args)

        self.command   = Path(os.environ["DEVKITARM"]) / "bin/arm-none-eabi-addr2line"
        self.arguments = "-aipfCe arm -e"

        if args.log:
            self.parse_log(args.log)
        else:
            self.addr2line(args.pc, args.lr)

    def parse_log(self, log):
        try:
            subprocess.run(f"luma3ds_exception_dump_parser {log}", shell=True)
        except Exception as exception:
            print(exception)