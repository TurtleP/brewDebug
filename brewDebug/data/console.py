import re
import subprocess
from pathlib import Path
import os


class Console:

    def __init__(self, elf_path, *, pc=None, lr=None):
        self.filename = elf_path

        self.bin_path = Path(os.environ["DEVKITARM"], "bin")
        if str(self) == "Switch":
            self.bin_path = Path(os.environ["DEVKITPRO"], "devkitA64", "bin")

        self.bin_name = re.search(r"(\w+\.elf)", elf_path).group(1)
        self.app_name = self.bin_name[:-4]

        self.pc = pc
        self.lr = lr

    def get_command(self):
        return f"{self.get_addr2line()} {self.get_addr2line_args()}" \
               f"{self.filename} {self.lr} {self.pc}"

    def run_debug(self):
        try:
            print()
            output = subprocess.run(self.get_command(), shell=True,
                                    capture_output=True)

            print(output.stdout.decode('utf-8'), end='')
        except Exception as e:
            print(str(e))
