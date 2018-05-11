'''
'''

import sys
from .app import App

class Command(App):
    '''
    A subcommand for multicommands cli tool
    '''
    command_name = None
    parent_config = None
    use_subconfig = False
    merge_parent_arguments = True

    def __str__(self):
        return "<ChudaCommand command_name={}>".format(self.command_name)

    def __repr__(self):
        return "<ChudaCommand command_name={}>".format(self.command_name)

    def __init__(self): # pylint: disable=W0231
        pass

    def setup(self, parent_arguments, parent_config, parent_logger):
        '''
        Setup properties from parent app on the command
        '''
        self.logger = parent_logger

        if self.command_name is None:
            self.logger.error("The command_name attribute is required")
            sys.exit(1)

        self.parent_config = parent_config
        self.arguments = parent_arguments

        if self.use_subconfig:
            self.__init_config()
        else:
            self.config = self.parent_config