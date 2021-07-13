import os
import strutils
import strformat

import re

type
    BinaryType* = enum
        AARCH64, ARM64, INVALID

type
    Config* = object
        addresses: tuple[pc: string, lr: string]
        log_path: string

        elf_path: string
        bin_type: BinaryType

var conf*: Config

proc binaryExists(path: string): bool =
    if not path.isEmptyOrWhitespace():
        return path.fileExists()

    echo(fmt("Binary does not exist at path {path}"))

    return false

proc getBinaryType(config: Config): BinaryType =
    if not binaryExists(config.elf_path):
        return BinaryType.INVALID

    let buffer = readFile(config.elf_path)
    let position = find(buffer, re("(aarch64)"))

    if position != -1:
        return BinaryType.AARCH64

    return BinaryType.ARM64

proc loadCommon(config: var Config, elf_path: string) =
    conf = Config()

    config.elf_path = expandTilde(normalizedPath(elf_path))
    config.bin_type = config.getBinaryType()

proc convertAddresses*(config : var Config, pc, lr : string) : tuple[pc, lr : string] =
    var addrs = (pc: parseHexInt(pc), lr: parseHexInt(lr))

    if (config.bin_type == BinaryType.AARCH64):
        addrs.pc -= 0x8

    return (pc: toHex(addrs.pc), lr: toHex(addrs.lr))

proc loadLog*(config: var Config, elf_path, log_path: string) =
    config.loadCommon(elf_path)

    config.log_path = log_path

proc loadAddress*(config: var Config, elf_path: string, addresses: tuple) =
    config.loadCommon(elf_path)

    config.addresses = config.convertAddresses(addresses.pc, addresses.lr)

proc getAddresses*(config: Config): tuple =
    return config.addresses

proc hasLog*(config: Config): bool =
    return config.log_path.fileExists()

proc getLogContent*(config: Config): string =
    let buffer = config.log_path.readFile()

    return buffer

proc getType*(config: Config): BinaryType =
    return config.bin_type

proc getBinaryName*(config: Config): string =
    if not binaryExists(config.elf_path):
        return ""

    let (_, name, _) = splitFile(config.elf_path)

    return name

proc getBinaryPath*(config: Config): string =
    if not binaryExists(config.elf_path):
        return ""

    return config.elf_path
