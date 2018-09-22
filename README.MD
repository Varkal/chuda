# Chuda #
![PyPI](https://img.shields.io/pypi/v/chuda.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chuda.svg)
![GitHub](https://img.shields.io/github/license/Varkal/chuda.svg)
[![Documentation Status](https://readthedocs.org/projects/chuda/badge/?version=latest)](https://chuda.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Varkal/chuda/branch/master/graph/badge.svg)](https://codecov.io/gh/Varkal/chuda)
[![CircleCI](https://circleci.com/gh/Varkal/chuda.svg?style=svg)](https://circleci.com/gh/Varkal/chuda)


**Chuda** is a very simple Python3 framework to create CLI (Command-Line-Interface) tools.

It will handle for you some basic stuff: parse configuration file, logging, argument parsing, signal handling etc...

## Features ##

* Represent commands and argparse arguments by Python classes
* Handle parsing of a configuration file for you (INI, JSON, or YAML with [pyyaml](https://github.com/yaml/pyyaml))
* Provide you a configurable logger, and some basic options to quiet/verbose mode
* Provide you a simple interface to run some shell commands
* Signals handling by decorator
* Integrates [argcomplete](https://argcomplete.readthedocs.io/en/latest/) by default

## Documentation ##

The documentation is accessible [here](http://chuda.readthedocs.io)

## Example ##

```python

import sys
import signal
from chuda import App, autorun, Command signal_handler, Option 


class FooSubcommand(Command):
    command_name = "foo"
    description = "a foo subcommand"

    def main(self):
        self.logger.info("foo")
        self.app.subcommands["bar"].run()


class BarSubcommand(Command):
    command_name = "bar"
    description = "the ultimate bar subcommand"

    arguments = [
        Option(name=["--path"], default="~")
    ]

    def main(self):
        process = self.shell.run(
            "ls", cwd=self.arguments.path
        )
        self.logger.info(process.output)


@autorun()
class FooBarApp(App):
    app_name = "foobar"
    description = "Foobar application"

    config_path = ["./config.ini", "../config.ini"]

    subcommands = [FooSubcommand, BarSubcommand]

    @signal_handler(signal.SIGINT)
    def handle_ctrl_c(self, signum, frame):
        self.logger.info("Stopping...")
        sys.exit(2)

```
