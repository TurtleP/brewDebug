import console
export console

import nre

import strformat
import strutils

import os
import osproc

import config

type CTR* = ref object of ConsoleBase

proc getCommandPath(self: CTR): string =
    getEnv("DEVKITARM") & "/bin/"

proc getCommand*(self: CTR): string =
    self.getCommandPath() & "arm-none-eabi-addr2line -aipfCe arm -e"

proc getLogParser(filepath: string): string =
    fmt("luma3ds_exception_dump_parser {filepath}")

proc parseLog(): tuple[pc, lr: string] =
    let res = execCmdEx(getLogParser(conf.getLogPath()))
    let buffer = res.output

    let lrRegister = re"lr\s+([A-z0-9]{8})"
    let pcRegister = re"pc\s+([A-z0-9]{8})"

    let lr = find(buffer, lrRegister).get().captures[0]
    let pc = find(buffer, pcRegister).get().captures[0]

    return (pc: pc, lr: lr)

proc runDebug*(self: CTR) =
    echo(fmt("[{getHeader()}]\n"))

    var values = conf.getAddresses()
    if conf.hasLog():
        values = parseLog()

    addr2line(self.getCommand(), @[values])

    echo("[" & repeat("=", len(getHeader())) & "]")
