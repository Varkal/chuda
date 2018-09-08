#!/usr/bin/env python
import sys
import signal
import os

sys.path.append('../chuda')
from chuda import App, autorun, Command, Plugin, signal_handler, Option, Parameter  # pylint: disable=C0413
from pathlib import Path


class ExampleSubcommand(Command):
    command_name = "foo"
    description = "a foo subcommand"

    def main(self):
        self.logger.info(self.arguments.path)
        self.app.subcommands["bar"].run()
        process = self.shell.run("ls", stdout=None)
        # self.logger.info(process.output)


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


# @autorun()
# class ExampleApp(App):
#     app_name = "example"
#     description = "example software"

#     # config_path = ["./config.yml", Path(os.path.abspath(__file__)) / "../config.yml"]
#     # config_parser = "yaml"

#     config_path = ["./config.ini", "../config.ini"]

#     plugins = [
#         Pipo()
#     ]

#     arguments = [
#         Option(name=["-t", "--test"], dest="test"),
#         Option(name=["-p", "--path"], default=Path(".") / "toto")
#     ]

#     subcommands = [ExampleSubcommand, ExampleSubcommand2]

#     @signal_handler(signal.SIGINT)
#     def handle_ctrl_c(self, signum, frame):  # pylint: disable=W0613
#         self.logger.info("ctrl_C")
#         sys.exit(2)

#     def main(self):
#         self.logger.info("Hello {}".format(self.config["hello"]["name"]))
#         self.logger.debug("debug")
#         self.logger.info("info")
#         self.logger.warning("warn")
#         self.logger.error("error")
#         self.logger.critical("critical")


from chuda import App, autorun, Plugin
import requests


class HttpPlugin(Plugin):
    base_url = None

    def on_create(self):
        self.enrich_app("http", self)

    def on_config_read(self):
        try:
            self.base_url = self.app.config["base_url"]
        except KeyError:
            self.base_url = "http://www.example.com"

    def get_root(self):
        return requests.get(self.base_url)


@autorun()
class HttpApp(App):
    http = None

    plugins = [
        HttpPlugin()
    ]

    def main(self):
        response = self.http.get_root()
        self.logger.info(response.text)
