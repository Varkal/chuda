import os
import argparse
import logging
import logging.config
import importlib
import signal
import argcomplete
import chuda.utils as utils
from .arguments import Option
from .plugins import Plugin
from .shell import Runner


class App:
    app_name = None
    arguments = []
    arguments_declaration = []
    config = {}
    config_parser = "ini"
    config_path = None
    default_arguments = [
        Option(
            name=["-q", "--quiet"], dest="quiet", action="store_true",
            help="make console output silent"
        ),
        Option(
            name=["-v", "--verbose"], dest="verbose", action="store_true",
            help="make console output more talkative"
        ),
        Option(
            name=["--version"], dest="version", action="store_true",
            help="show version and exit"
        )
    ]
    description = None
    logger = None
    override_default_arguments = False
    parser = None
    plugins = []
    shell = Runner()
    subcommands = []
    version = "0.0.1"

    __signal_handlers = {}

    def __str__(self):
        return "<ChudaApp app_name={}>".format(self.app_name)

    def __repr__(self):
        return "<ChudaApp app_name={}>".format(self.app_name)

    def in_autocomplete_mode(self):
        return "_ARGCOMPLETE" in os.environ

    def __init_arguments(self):
        self.parser = argparse.ArgumentParser(
            prog=self.app_name,
            description=self.description
        )

        self.parser.set_defaults(command="main")

        if not self.override_default_arguments:
            self.arguments = self.default_arguments + self.arguments

        for argument in self.arguments:
            arg_tuple = argument.convert_to_argument()
            if isinstance(arg_tuple[0], list):
                parg = self.parser.add_argument(*arg_tuple[0], **arg_tuple[1])
            else:
                parg = self.parser.add_argument(arg_tuple[0], **arg_tuple[1])

            if argument.completer:
                parg.completer = argument.completer

        subcommands_dict = {}
        if self.subcommands:
            subparsers = self.parser.add_subparsers(
                title="subcommands"
            )

        for subcommand in self.subcommands:
            instance = subcommand()
            subcommands_dict[instance.command_name] = instance
            subparser = subparsers.add_parser(
                instance.command_name,
                help=instance.description,
                description=instance.description
            )
            subparser.set_defaults(command=instance.command_name)
            if instance.merge_parent_arguments:
                instance.arguments = self.arguments + instance.arguments

            for argument in instance.arguments:
                arg_tuple = argument.convert_to_argument()
                if isinstance(arg_tuple[0], list):
                    sp_arg = subparser.add_argument(*arg_tuple[0], **arg_tuple[1])
                else:
                    sp_arg = subparser.add_argument(arg_tuple[0], **arg_tuple[1])

                if argument.completer:
                    sp_arg.completer = argument.completer

        argcomplete.autocomplete(
            argument_parser=self.parser,
            always_complete_options=False
        )

        self.arguments_declaration = self.arguments
        self.arguments = self.parser.parse_args()
        self.subcommands = subcommands_dict

    def __init_config(self):
        if self.config_path:
            config_path_list = []
            if isinstance(self.config_path, str):
                config_path_list = [self.config_path]
            elif isinstance(self.config_path, list):
                config_path_list = self.config_path

            for path in config_path_list:
                if os.path.isfile(path):
                    self.config_path = path
                    break
                else:
                    self.config_path = None

            if self.config_path:
                if self.config_parser.lower() == "ini":
                    configparser = importlib.import_module("configparser")
                    tmp = configparser.ConfigParser()
                    tmp.read(self.config_path)
                    for section in tmp.sections():
                        utils.dict_merge(self.config, {section: tmp[section]})

                if self.config_parser.lower() == "yaml":
                    yaml = importlib.import_module("yaml")
                    with open(self.config_path, "r") as file:
                        tmp = yaml.load(file.read())
                        utils.dict_merge(self.config, tmp)

                if self.config_parser.lower() == "json":
                    json = importlib.import_module("json")
                    with open(self.config_path, "r") as file:
                        tmp = json.load(file)
                        utils.dict_merge(self.config, tmp)

    def __init_logging(self):
        logging_config = utils.DEFAULT_LOGGER_CONFIG
        if self.config.get("logging", None):
            utils.dict_merge(logging_config, self.config["logging"])

        if utils.get_flag(self.arguments, "verbose"):
            for name, handler in logging_config.get("handlers", {}).items():
                handler["level"] = "DEBUG"
                logging_config["handlers"][name] = handler

            for name, logger in logging_config.get("loggers", {}).items():
                logger["level"] = "DEBUG"
                logging_config["loggers"][name] = logger

        self.config["logging"] = logging_config
        logging.config.dictConfig(self.config["logging"])

        if utils.get_flag(self.arguments, "quiet"):
            self.logger = utils.Null()
        else:
            self.logger = logging.getLogger("default")

        self.shell.logger = self.logger

    def __init_plugins(self):
        instances = []

        for plugin in self.plugins:
            if isinstance(plugin, type):
                instance = plugin()
                if not isinstance(plugin, Plugin):
                    raise TypeError("plugins should subclasse the Plugin class")
                instance.setup(self)
                instances.append(instance)
            elif isinstance(plugin, Plugin):
                plugin.setup(self)
                instances.append(plugin)
            else:
                raise TypeError("plugins should subclasse the Plugin class")

        instances.sort(key=lambda p: p.priority)

        self.plugins = instances

    def call_plugins(self, step):
        '''
        Check if a 'step' method exist on each plugin, and call it
        '''
        for plugin in self.plugins:
            try:
                getattr(plugin, step)()
            except AttributeError:
                self.logger.debug("{} doesn't exist on plugin {}".format(step, plugin))
            except TypeError:
                self.logger.debug("{} on plugin {} is not callable".format(step, plugin))

    def __init_signals(self):
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            handle_signal = getattr(attribute, "handle_signal", None)
            if handle_signal:
                self.__signal_handlers \
                    .setdefault(handle_signal, []) \
                    .append(attribute)

        for plugin in self.plugins:
            for attribute_name in dir(plugin):
                attribute = getattr(plugin, attribute_name)
                handle_signal = getattr(attribute, "handle_signal", None)
                if handle_signal:
                    self.__signal_handlers \
                        .setdefault(handle_signal, []) \
                        .append(attribute)

        for key in self.__signal_handlers:
            signal.signal(key, self.__signal_handler_factory(key))

    def __signal_handler_factory(self, sig):
        def __signal_handler(signum, frame):
            for handler in self.__signal_handlers[sig]:
                handler(signum, frame)

        return __signal_handler

    def __init__(self):
        self.__init_plugins()
        self.call_plugins("on_create")
        self.__init_signals()
        self.call_plugins("on_signals_handled")
        self.__init_config()
        self.call_plugins("on_config_read")
        self.__init_arguments()
        self.call_plugins("on_arguments_parsed")
        self.__init_logging()
        self.call_plugins("on_logger_created")
        self.__setup_subcommands()

    def __setup_subcommands(self):
        for _, command in self.subcommands.items():
            command.setup(self)

    def run(self):
        self.call_plugins("on_run")
        if vars(self.arguments).get("version", None):
            self.logger.info("{app_name}: {version}".format(app_name=self.app_name, version=self.version))
        else:
            if self.arguments.command == "main":
                self.main()
            else:
                self.subcommands[self.arguments.command].run()
        self.call_plugins("on_end")

    def main(self):
        if not utils.get_flag(self.arguments, "quiet"):
            self.parser.print_help()
