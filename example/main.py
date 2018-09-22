#!/usr/bin/env python
import sys
import signal
import os

sys.path.append('../chuda')
from chuda import App, autorun, Command, Plugin, signal_handler, Option, Parameter  # pylint: disable=C0413
from pathlib import Path


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
