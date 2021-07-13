import osproc

import iface
import strformat

type ConsoleBase* = ref object of RootObj

iface *Console:
    proc getCommand(): string
    proc runDebug()

proc addr2line*(command: string, addresses: seq[tuple]): bool =

    try:
        var results: seq[string]

        for address in addresses:
            let output = execCmdEx(fmt("{command} {conf.getBinaryPath()} {address.pc} {address.lr}"))
            results.add(output.output)

        echo(fmt("[Debugging Results for {conf.getBinaryName()}]\n"))

        for output in results:
            echo(output)
    except Exception as e:
        echo(e.msg)
        return false

    return true
