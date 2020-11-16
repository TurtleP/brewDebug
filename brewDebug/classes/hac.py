import os
import re
from pathlib import Path

from .console import Console


class HAC(Console):

    def __init__(self, filepath, args):
        super().__init__(filepath)

        self.command   = Path(os.environ["DEVKITPRO"]) / "devkitA64/bin/aarch64-none-elf-addr2line"
        self.arguments = "-aipfCe"

        if args.log:
            self.parse_log(args.log)
        else:
            self.addr2line(args.pc, args.lr)

    def parse_log(self, log):
        location_search = re.compile(r"(0x[0-9a-fA-F]+)")

        with open(log, "r", encoding="utf-8") as file:
            found_items = re.findall(f"PC.*|LR.*{self.name}.+", file.read(), re.MULTILINE)

            for index in range(0, len(found_items), 2):
                lr = location_search.search(found_items[index]).group(0)
                pc = location_search.search(found_items[index + 1]).group(0)

                self.addr2line(pc, lr, (index + 2) % len(found_items))