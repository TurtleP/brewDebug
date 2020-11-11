import os
import shutil
import subprocess
from pathlib import Path

from .console import Console


class CTR(Console):

    def __init__(self, args):
        super().__init__(args)

        self.command   = Path(os.environ["DEVKITARM"]) / "bin/arm-none-eabi-addr2line"
        self.arguments = "-aipfCe arm -e"

        self.log_parser = "luma3ds_exception_dump_parser"

        if args.log:
            self.parse_log(args.log)
        else:
            self.addr2line(args.pc, args.lr)

    def parse_log(self, log):
        if shutil.which(self.log_parser) is None:
            return print("error: luma3ds exception parser not installed.")

        try:
            subprocess.run(f"{self.log_parser} {log}", shell=True)
        except Exception as exception:
            print(exception)
