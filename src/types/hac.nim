import console
export console

import os
import nre
import strformat
import strutils

import config

type HAC* = ref object of ConsoleBase

proc getCommandPath(self: HAC): string =
    getEnv("DEVKITPRO") & "/devkitA64/bin/"

proc getCommand*(self: HAC): string =
    self.getCommandPath() & "aarch64-none-elf-addr2line -aipfCe"

proc parseLog(): seq[tuple[pc, lr: string]] =
    let buffer = conf.getLogContent()

    let addressSearch = re(r"(0x[0-9a-fA-F]+)")

    let name = conf.getBinaryName()
    let registerSearch = re(fmt("PC.*{name}.+|LR.*{name}.+"))

    let found = findAll(buffer, registerSearch)

    if len(found) == 0:
        return @[(pc: "", lr: "")]

    var results: seq[tuple[pc, lr: string]]
    for index in countup(0, len(found) - 1, 2):
        let lr = find(found[index], addressSearch).get().match()
        let pc = find(found[index + 1], addressSearch).get().match()

        let values = conf.convertAddresses(pc, lr)

        results.add(values)

    return results

proc runDebug*(self: HAC) =
    echo(fmt("[{getHeader()}]\n"))

    if conf.hasLog():
        let addresses = parseLog()

        for addrPair in addresses:
            addr2line(self.getCommand(), @[addrPair])
    elif conf.hasBacktrace():
        addr2line(self.getCommand(), conf.getBacktrace())
    else:
        addr2line(self.getCommand(), @[conf.getAddresses()])

    echo("[" & repeat("=", len(getHeader())) & "]")
