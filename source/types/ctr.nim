import console
export console

import os

import config

type CTR* = ref object of ConsoleBase

proc getCommandPath(self: CTR): string = getEnv("DEVKITARM") & "/bin/"
proc getCommand*(self: CTR): string = self.getCommandPath() & "arm-none-eabi-addr2line -aipfCe arm -e"

proc parseLog(): seq[string] =
    return @[""]

proc runDebug*(self: CTR) =
    var results: bool

    if conf.hasLog():
        let values = parseLog()
    else:
        results = addr2line(self.getCommand(), @[conf.getAddresses()])
