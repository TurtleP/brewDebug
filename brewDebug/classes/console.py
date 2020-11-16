import subprocess
from pathlib import Path


class Console:

    def __init__(self, file):
        self.binary = Path(file)
        self.name   = self.binary.name[:-4]

    def addr2line(self, pc, lr, newline=True):
        print(f"[Debugging Results for {self.name}]\n")

        try:
            subprocess.run(f"{self.command} {self.arguments} {self.binary} {pc} {lr}", shell=True)

            if newline:
                print()
        except Exception as exception:
            print(exception)
