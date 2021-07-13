import console
export console

import os
import re
import strformat

import config

type HAC* = ref object of ConsoleBase

proc getCommandPath(self: HAC): string = getEnv("DEVKITPRO") & "/devkitA64/bin"
proc getCommand*(self: HAC): string = self.getCommandPath() & "/aarch64-none-elf-addr2line -aipfCe"

proc parseLog(): seq[string] =
    let buffer = conf.getLogContent()

    let addressSearch = re(r"(0x[0-9a-fA-F]+)")

    let name = conf.getBinaryName()
    let registerSearch = re(fmt("PC.*|LR.*{name}.+"))

    let found = findAll(buffer, registerSearch)

    if len(found) == 0:
        return @[""]

    echo found

proc runDebug*(self: HAC) =
    var results: bool

    if conf.hasLog():
        let items = parseLog()
    else:
        results = addr2line(self.getCommand(), @[conf.getAddresses()])
