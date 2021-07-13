import strutils
import strformat

import types/config

import cligen

import types/hac
import types/ctr

import os
import parsetoml

let CONFIG_FILE_DIR = expandTilde(normalizedPath(getConfigDir() &
        "/.brewDebug"))
let CONFIG_FILE_PATH = normalizedPath(CONFIG_FILE_DIR & "/config.toml")

const VERSION = "0.4.0"

template loadConsoleChild(child: type): untyped =
    console = child()

proc pathFromConfigFile(key: string): string =
    ## If the key exists, return its value

    if key.contains(":"):
        let split = key.split(":")
        if CONFIG_FILE_PATH.fileExists():
            let toml = parseToml.parseFile(CONFIG_FILE_PATH)
            let value = toml[split[0]][split[1]].getStr()

            if value.isEmptyOrWhitespace():
                echo(fmt("Cannot parse {key}. Config value does not exist."))
                return ""

            return value
        else:
            echo(fmt("Cannot parse {key}. Config file does not exist."))

    return key

proc execute() =
    var console: Console
    let fileType = conf.getType()

    if fileType == BinaryType.INVALID:
        return

    case fileType:
        of BinaryType.AARCH64:
            HAC.loadConsoleChild()
        else:
            CTR.loadConsoleChild()

    console.runDebug()

proc log(elf_path, log_path: string): Console =
    ## Read from a log file

    let path = pathFromConfigFile(elf_path)
    conf.loadLog(path, log_path)

    execute()

proc addresses(elf_path: string, pc, lr: string) =
    ## Debug from PC and LR

    let path = pathFromConfigFile(elf_path)

    var addresses = (pc: parseHexInt(pc), lr: parseHexInt(lr))
    conf.loadAddress(path, addresses)

    execute()

proc version() =
    ## Print version information and exit

    echo(fmt("brewDebug {VERSION}"))

# proc backtrace(start, bt : string) =
#     ## Debug from fatal "Backtrace - Start Address"

if not CONFIG_FILE_DIR.dirExists():
    CONFIG_FILE_DIR.createDir()

dispatchMulti([log], [addresses], [version])
