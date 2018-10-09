import sys
from .utils import _init_config
from .arguments import Option, Parameter
from .shell import Runner
from .exceptions import EmptyCommandNameException, ArgumentNotFoundException


class Command:
    '''
    A subcommand for multicommands cli tool
    '''

    #: Name of the command, use on the command-line (like "add", in "git add")
    command_name = None

    #: Should use config_parser and config_path to generate a config for this command
    use_subconfig = False

    #: The configuration file will be loaded here
    config = {}

    #: The parser used to parse the configuration file.
    #: Possible values are: ini, json, yaml
    config_parser = "ini"

    #: Acceptable paths to find the configuration file.
    #: Stop searching on the first one exists
    config_path = []

    #: Contains a reference to the :class:`~chuda.app.App` instance who contains this Command
    app = None

    #: Should parent arguments be merge with local arguments ? True by default.
    merge_parent_arguments = True

    #: List of :class:`~chuda.arguments.Argument` objects. Replace with the argparse.Namespace at runtime
    arguments = []

    #: | :attr:`~chuda.app.App.arguments` will be copied here of before it be replaced with namespace
    #: | **Warning**: This will contains **only** local arguments declarations
    arguments_declaration = None

    #: Instance of :class:`~logging.Logger`
    logger = None

    #: Instance of :class:`~chuda.shell.Runner`
    shell = Runner()

    def __str__(self):
        return "<ChudaCommand command_name={}>".format(self.command_name)

    def __repr__(self):
        return "<ChudaCommand command_name={}>".format(self.command_name)

    def __init__(self):  # pylint: disable=W0231
        pass

    def main(self):
        pass

    def __check_arguments(self):
        try:
            for declaration in self.arguments_declaration:
                if declaration.dest:
                    name = declaration.dest
                elif isinstance(declaration, Option):
                    name = declaration.get_default_name()
                elif isinstance(declaration, Parameter):
                    name = declaration.name

                value = getattr(self.arguments, name, None)

                if value is None and declaration.required:
                    raise ArgumentNotFoundException(name)
                elif value is None:
                    default = getattr(declaration, "default", None)
                    setattr(self.arguments, name, default)

        except ArgumentNotFoundException as error:
            self.logger.error("Cannot run \"{}\" command : \n\t{}".format(self.command_name, error))
            raise error

        return True

    def run(self):
        """
        Run the command
        """
        if self.__check_arguments():
            self.main()

    def setup(self, app):
        '''
        Setup properties from parent app on the command
        '''
        self.logger = app.logger
        self.shell.logger = self.logger

        if not self.command_name:
            raise EmptyCommandNameException()

        self.app = app
        self.arguments_declaration = self.arguments
        self.arguments = app.arguments

        if self.use_subconfig:
            _init_config(self)
        else:
            self.config = self.app.config
