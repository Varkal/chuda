#!/usr/bin/env python
import sys
import signal
import os

sys.path.append('../chuda')
from chuda import App, autorun, Command, Plugin, signal_handler, Option, Parameter # pylint: disable=C0413


class ExampleSubcommand(Command):
    command_name = "foo"
    description = "a foo subcommand"

    def main(self):
        process = self.shell.run("ls", cwd="/")
        command = self.app.subcommands["bar"]
        command.arguments.protocol = "http"
        self.logger.info(process.output)
        command.run()


class ExampleSubcommand2(Command):
    command_name = "bar"
    description = "the ultimate bar subcommand"

    arguments = [
        Parameter(name="protocol", nargs="?")
    ]

    def main(self):
        self.logger.info(self.arguments.protocol)


class Pipo(Plugin):
    def on_create(self):
        self.enrich_app("pipo", 12)


@autorun()
class ExampleApp(App):
    app_name = "example"
    description = "example software"

    config_path = ["./config.yml", os.path.dirname(os.path.abspath(__file__))+"/config.yml"]
    config_parser = "yaml"

    plugins = [
        Pipo()
    ]

    arguments = [
        Option(name=["-t", "--test"], dest="test")
    ]

    subcommands = [ExampleSubcommand, ExampleSubcommand2]

    @signal_handler(signal.SIGINT)
    def handle_ctrl_c(self, signum, frame):  # pylint: disable=W0613
        self.logger.info("ctrl_C")
        sys.exit(2)

    def main(self):
        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warn")
        self.logger.error("error")
        self.logger.critical("critical")
