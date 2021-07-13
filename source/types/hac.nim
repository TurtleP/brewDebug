import console
export console

import os

import config

type HAC* = ref object of ConsoleBase

proc getCommandPath(self: HAC): string = getEnv("DEVKITPRO") & "/devkitA64/bin"
proc getCommand*(self: HAC): string = self.getCommandPath() & "/aarch64-none-elf-addr2line -aipfCe"

proc runDebug*(self: HAC) =
    let results = addr2line(self.getCommand(), @[conf.getAddresses()])
