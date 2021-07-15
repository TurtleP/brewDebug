import strformat
import strutils

import os

import types/config

import types/ctr
import types/hac

import cligen; include cligen/mergeCfgEnv
import parsetoml

let CONFIG_FILE_DIR = expandTilde(normalizedPath(getConfigDir() &
        "/.brewDebug"))
let CONFIG_FILE_PATH = normalizedPath(CONFIG_FILE_DIR & "/config.toml")

const version = staticRead("../brewDebug.nimble").fromNimble("version")
clCfg.version = fmt("brewDebug {version}")

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

proc execute(fileType: BinaryType) =
    ## Execute debugging for the file type

    var console: Console

    if fileType == BinaryType.INVALID:
        echo("Invalid ELF binary was found. Check your path and try again.")
        return

    case fileType:
        of BinaryType.AARCH64:
            HAC.loadConsoleChild()
        else:
            CTR.loadConsoleChild()

    console.runDebug()

proc findEnvVar(name: string): bool =
    ## Check if an environment variable exists.
    ## If it doesn't, display an error

    if not existsEnv(name):
        echo(fmt("Could not find environment variable {name}. Make sure it's in your PATH!"))
        return false

    return true

proc findBinary(name: string): bool =
    ## Check if a binary exists.
    ## If it doesn't, display an error

    if findExe(name).isEmptyOrWhitespace():
        var package = "devkitARM"

        if "aarch64" in name:
            package = "devkitA64"

        echo(fmt("Could not find executable {name}. Please install {package} from devkitpro-pacman."))
        return false

    return true

proc checkEnvironment(fileType: BinaryType): bool =
    ## Check if something we need exists for the binary type.
    ## If it doesn't, display an error

    case fileType:
        of AARCH64:
            if findEnvVar("DEVKITPRO"):
                return findBinary("aarch64-none-elf-addr2line")
        of ARM64:
            if findEnvVar("DEVKITARM"):
                return findBinary("arm-none-eabi-addr2line")
        of INVALID:
            return false

    return false

proc log(elf_path, log_path: string) =
    ## Read from a log file

    let path = pathFromConfigFile(elf_path)
    conf.loadLog(path, log_path)

    let fileType = conf.getType()
    if fileType == BinaryType.ARM64:
        if findExe("luma3ds_exception_dump_parser").isEmptyOrWhitespace():
            echo("Please install the Luma3DS Exception Parser")
            return

    if checkEnvironment(fileType):
        execute(fileType)
    else:
        quit(-1)

proc addresses(elf_path, pc, lr: string) =
    ## Debug from PC and LR

    let path = pathFromConfigFile(elf_path)
    conf.loadAddress(path, (pc: pc, lr: lr))

    let fileType = conf.getType()

    if checkEnvironment(fileType):
        execute(fileType)
    else:
        quit(-1)

proc backtrace(elf_path, backtrace, start: string) =
    ## Debug from fatal "Backtrace - Start Address", Nintendo Switch only

    let path = pathFromConfigFile(elf_path)

    let hexBacktrace = parseHexInt(backtrace)
    let hexStart = parseHexInt(start)

    let resBacktrace = toHex(hexBacktrace - hexStart)

    conf.loadBacktrace(path, resBacktrace)
    let fileType = conf.getType()

    if fileType != BinaryType.AARCH64:
        echo("Cannot use backtrace with non-aarch64 binary")
        return

    if checkEnvironment(fileType):
        execute(fileType)
    else:
        quit(-1)

when isMainModule:
    if not CONFIG_FILE_DIR.dirExists():
        CONFIG_FILE_DIR.createDir()

    dispatchMulti([log], [addresses], [backtrace])
