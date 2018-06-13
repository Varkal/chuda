import sys
from .utils import _init_config
from .arguments import Option, Parameter
from .shell import Runner


class Command:
    '''
    A subcommand for multicommands cli tool
    '''
    command_name = None
    parent_config = None
    use_subconfig = False
    app = None
    merge_parent_arguments = True
    arguments = []
    arguments_declaration = None
    logger = None
    config = {}
    shell = Runner()

    def __str__(self):
        return "<ChudaCommand command_name={}>".format(self.command_name)

    def __repr__(self):
        return "<ChudaCommand command_name={}>".format(self.command_name)

    def __init__(self):  # pylint: disable=W0231
        pass

    def main(self):
        pass

    def check_arguments(self):
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
                    raise AttributeError("Argument {} not found".format(name))
                elif value is None:
                    default = getattr(declaration, "default", None)
                    setattr(self.arguments, name, default)

        except AttributeError as error:
            self.logger.error("Cannot run \"{}\" command : \n\t{}".format(self.command_name, error))
            return False

        return True

    def run(self):
        if self.check_arguments():
            self.main()

    def setup(self, app):
        '''
        Setup properties from parent app on the command
        '''
        self.logger = app.logger
        self.shell.logger = self.logger

        if self.command_name is None:
            self.logger.error("The command_name attribute is required")
            sys.exit(1)

        self.app = app
        self.parent_config = app.config
        self.arguments_declaration = self.arguments
        self.arguments = app.arguments

        if self.use_subconfig:
            _init_config(self)
        else:
            self.config = self.parent_config
