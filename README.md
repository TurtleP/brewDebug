<<<<<<< HEAD
## brewDebug

Nintendo Homebrew ELF debugging utility.

## Installation

The easiest way to "install" brewDebug is from the releases page. Download the respective platform's release and put it in the following directory for your operating system:

    Windows: %appdata%/.brewDebug/bin
        Create this directory and add it to your PATH!
    Linux: /usr/bin
    macOS: TBD

## Command Line

You can use the commands below to debug an exception on 3DS or Switch.

```
Usage:
  brewDebug {SUBCMD}  [sub-command options & parameters]
where {SUBCMD} is one of:
  help       print comprehensive or per-cmd help
  log        Read from a log file
  addresses  Debug from PC and LR
  version    Print version information and exit

brewDebug {-h|--help} or with no args at all prints this message.
brewDebug --help-syntax gives general cligen syntax help.
Run "brewDebug {help SUBCMD|SUBCMD --help}" to see help for just SUBCMD.
Run "brewDebug help" to get *comprehensive* help.
```

Alternatively, instead of providing a full path to the ELF binary, one can create a `config.toml` file under the `config` directory for their OS:

* Windows: `%appdata%/.brewDebug`
* macOS & Linux: `~/.config/.brewDebug`

For example, take this config structure:

```toml
[LOVEPotion]
3DS = "~/GitHub/lovepotion/platform/3ds/LOVEPotion.elf"
Switch = "~/GitHub/lovepotion/platform/switch/LOVEPotion.elf"
```

When asking for the elf_path, simply provide the `Table:Key` pair for this document. This example would be `LOVEPotion:3DS` or `LOVEPotion: Switch` . The colon ( `:` ) delimeter is the only one supported.
=======
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
>>>>>>> origin/master
