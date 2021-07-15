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
  backtrace  Debug from fatal "Backtrace - Start Address", Nintendo Switch only

brewDebug {-h|--help} or with no args at all prints this message.
brewDebug --help-syntax gives general cligen syntax help.
Run "brewDebug {help SUBCMD|SUBCMD --help}" to see help for just SUBCMD.
Run "brewDebug help" to get *comprehensive* help.
Top-level --version also available
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
