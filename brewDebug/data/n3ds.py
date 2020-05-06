import re
import subprocess

from .console import Console


class N3DS(Console):
    REGEX = r"\s+([0-9A-Fa-f]{8})"

    def __init__(self, elf_path, *, pc=None, lr=None, log_path=None):
        super().__init__(elf_path, pc=pc, lr=lr)

        if log_path:
            self.parse_log(log_path)

    def get_addr2line(self):
        return self.bin_path / "arm-none-eabi-addr2line"

    def get_addr2line_args(self):
        return "-aipfCe arm -e"

    def parse_log(self, log_path):
        process = None
        output = None

        try:
            process = subprocess.run(
                f"luma3ds_exception_dump_parser {log_path}",
                shell=True,
                capture_output=True
            )
        except Exception:
            print("Exception parser not installed.")

        if process is not None:
            output = process.stdout.decode('utf-8')

            if output is not None:
                fmt = "lr" + N3DS.REGEX
                self.lr = re.findall(fmt, output)[0]

                fmt = "pc" + N3DS.REGEX
                self.pc = re.findall(fmt, output)[0]

    def __str__(self):
        return "N3DS"
