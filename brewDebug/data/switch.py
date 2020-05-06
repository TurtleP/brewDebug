import re

from .console import Console


class Switch(Console):
    def __init__(self, elf_path, *, pc=None, lr=None, log_path=None):
        super().__init__(elf_path, pc=pc, lr=lr)

        self.link_list = []
        self.prog_list = []

        if log_path is not None:
            self.parse_log(log_path)

    def get_addr2line(self):
        return self.bin_path / "aarch64-none-elf-addr2line"

    def get_addr2line_args(self):
        return "-aipfCe"

    def _filter(self, register, value):
        res = re.findall(rf"{register}.*$", value, re.MULTILINE)
        sstring = rf"\({self.app_name} \+ (0x[0-9a-fA-F]+)\)"
        ret = []

        for item in res:
            search = re.search(sstring, item)
            ret.append(search.group(1))

        return ret

    def parse_log(self, path):
        with open(path, "r") as file:
            contents = file.read()

            self.link_list = self._filter("LR", contents)
            self.prog_list = self._filter("PC", contents)

    def __str__(self):
        return "Switch"

    def run_debug(self):
        if len(self.link_list) > 0:
            for link, prog in zip(self.link_list, self.prog_list):
                self.lr = link
                self.pc = prog

                super().run_debug()
        else:
            super().run_debug()
