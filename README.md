# brewDebug
Atmosphère &amp; Luma3DS Exceptions Parser

## Setup
1. install devkitPro's switch-tools and 3dstools packages from [`devkitPro-pacman`](https://devkitpro.org/wiki/devkitPro_pacman)
2. pip install -U git+https://github.com/LumaTeam/luma3ds_exception_dump_parser.git

## Installation
pip install -U git+https://github.com/TurtleP/brewDebug.git

## Config File

The config file is optional and can be created at `{HOME}/.config/brewDebug/config.toml`.

```toml
[App]
hac = "path/to/app.elf"
ctr = "path/to/app.elf"
```

## Usage

If a config file is present, it will instead ask for a `console` (hac or ctr) instead of `elf` path.
When there is more than one App entry inside the config, the `--app` optional argument is added.
This argument will default to the first entry in the config file unless specified.

```
usage: brewDebug [-h] [--pc PC] [--lr LR] [--log LOG] [--version] elf

Debugging utility for libctru and libnx homebrew ELF binaries.

positional arguments:
  elf            ELF binary

optional arguments:
  -h, --help     show this help message and exit
  --log LOG      The Log file dump.
  --version, -v  show program's version number and exit

exception registers:
  --pc PC        The Program Counter value
  --lr LR        The Link Register value
```


NOTE: `--log` cannot be used with the `--lr` or `--pc` arguments.
