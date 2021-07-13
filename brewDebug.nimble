# Package

version     = "0.1.0"
author      = "TurtleP"
description = "Nintendo 3DS & Switch Debugger"
license     = "MIT"
srcDir      = "source"
bin         = @["brewDebug"]
binDir      = "dist"


# Dependencies

requires "nim >= 1.5.0"
requires "parsetoml"
requires "cligen"
requires "https://github.com/yglukhov/iface"
