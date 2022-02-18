# Package

version = "0.2.0"
author = "TurtleP"
description = "Nintendo 3DS & Switch Debugger"
license = "MIT"

binDir = "dist"
srcDir = "src"
bin = @["brewDebug"]


# Dependencies

requires "nim >= 1.5.1"
requires "parsetoml"
requires "cligen"
requires "https://github.com/yglukhov/iface"
