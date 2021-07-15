import iface

import osproc
import strformat
import unicode

import config

type ConsoleBase* = ref object of RootObj

iface *Console:
    proc getCommand(): string
    proc runDebug()

proc getHeader*(): string =
    fmt("Debug Results for {conf.getBinaryName()}").toUpper()

proc addr2line*(command, address: string) =
    let res = execCmdEx(fmt("{command} {conf.getBinaryPath()} {address}"))

    echo(res.output)

proc addr2line*(command: string, addresses: seq[tuple]) =
    var results: seq[string]

    for address in addresses:
        let res = execCmdEx(fmt("{command} {conf.getBinaryPath()} {address.pc} {address.lr}"))
        results.add(res.output)

    for output in results:
        echo(output)
