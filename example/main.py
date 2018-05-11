#!/usr/bin/env python
import sys
import signal
import os

sys.path.append('../chuda')
from chuda import App, autorun, Command, Plugin, signal_handler, Option, Parameter



class ExampleSubcommand(Command):
    command_name = "foo"
    description = "a foo subcommand"

    def main(self):
        process = self.shell.run("ls")
        self.logger.info(process.out)

class ExampleSubcommand2(Command):
    command_name = "bar"
    description = "the ultimate bar subcommand"

    arguments = [
        Parameter(name="protocol", choices=["http", "https", "ftp", "sftp"])
    ]

    def main(self):
        self.logger.info(self.arguments.message)


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
        Option(name=["-t", "--test"], dest="test", default="empty")
    ]

    subcommands = [ExampleSubcommand, ExampleSubcommand2]

    @signal_handler(signal.SIGINT)
    def handle_ctrl_c(self, signum, frame): #pylint: disable=W0613
        print("ctrl_C")
        sys.exit(2)

    def main(self):
        self.logger.debug("test")
        self.logger.info(self.app_name)
        self.logger.info(self.arguments.test)
        self.logger.info(self.pipo) #pylint: disable=E1101
        self.logger.info(self.config["myconfig"]["a"])

        # signal.pause()
