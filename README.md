# brewDebug
Atmosphère &amp; Luma3DS Exceptions Parser

## Setup
1. install devkitPro's switch-tools and 3dstools packages from [`devkitPro-pacman`](https://devkitpro.org/wiki/devkitPro_pacman)
2. pip install -U git+https://github.com/LumaTeam/luma3ds_exception_dump_parser.git

## Installation
pip install -U git+https://github.com/TurtleP/brewDebug.git


## Usage
```
brewDebug [-h] [--pc PC] [--lr LR] [--log LOG] [--version] elf

Debugging utility for libctru and libnx homebrew ELF binaries.

positional arguments:
  elf            ELF binary

optional arguments:
  -h, --help     show this help message and exit
  --pc PC        The Program Counter value
  --lr LR        The Link Register value
  --log LOG      The Log file dump.
  --version, -v  show program's version number and exit
```

NOTE: `--log` cannot be used with the `--lr` or `--pc` arguments.