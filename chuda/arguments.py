'''
Module with argparse utils for chuda
'''
import argparse

from enum import Enum
from pathlib import Path
from .utils import to_snake_case


class ArgumentQuantity(Enum):
    OPTIONAL = "?"
    MULTIPLE = "+"
    MULTIPLE_OPTIONAL = "*"
    REMAINDER = argparse.REMAINDER


class Argument:
    '''
    Abstract parent class for :class:`~chuda.arguments.Option` and :class:`~chuda.arguments.Parameter`.

    For attributes who are not documented here, please see :meth:`~argparse.ArgumentParser.add_argument` documentation
    '''

    name = None
    action = "store"
    nargs = None
    const = None
    default = None
    type = None
    choices = None
    required = None
    help = None
    metavar = None
    dest = None

    #: Callable use by argcomplete to generate auto completion
    #: (see `arcomplete documentation <https://argcomplete.readthedocs.io/en/latest/#specifying-completers>`_)
    completer = None

    def __init__(self, name=None, action="store", nargs=None, const=None,
                 default=None, type=None, choices=None, required=None, help=None,  # pylint: disable=W0622
                 metavar=None, dest=None, completer=None):
        args = locals().copy()
        for key, value in args.items():
            if isinstance(value, Path):
                locals()[key] = str(value)

        self.name = name
        self.action = action
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar
        self.dest = dest
        self.completer = completer

    def convert_to_argument(self):
        '''
            Convert the Argument object to a tuple use in :meth:`~argparse.ArgumentParser.add_argument` calls on the parser
        '''

        field_list = [
            "action", "nargs", "const", "default", "type",
            "choices", "required", "help", "metavar", "dest"
        ]

        return (
            self.name,
            {
                field: getattr(self, field) for field in field_list if getattr(self, field) is not None
            }
        )


class Option(Argument):
    '''
    Represent an option on the command-line (``mycommand --whatever``)

    Attributes:
        name (list): Options can have multiple names, so name **must** be a list or a tuple
    '''

    def __repr__(self):  # pragma: no cover
        return "<Option name={}>".format(self.name)

    def __str__(self):  # pragma: no cover
        return "<Option name={}>".format(self.name)

    def get_default_name(self):
        '''
        Return the default generated name to store value on the parser for this option.

        eg. An option *['-s', '--use-ssl']* will generate the *use_ssl* name

        Returns:
            str: the default name of the option
        '''
        long_names = [name for name in self.name if name.startswith("--")]
        short_names = [name for name in self.name if not name.startswith("--")]

        if long_names:
            return to_snake_case(long_names[0].lstrip("-"))

        return to_snake_case(short_names[0].lstrip("-"))

    def convert_to_argument(self):
        if not isinstance(self.name, list) and not isinstance(self.name, tuple):
            raise TypeError("Inapropriate name type for Option. Should be a tuple or a list")

        if not self.name:
            raise ValueError("Name list cannot be empty")

        return super(Option, self).convert_to_argument()


class Parameter(Argument):
    '''
    Represent a parameter on the command-line (``mycommand whatever``)

    Attributes:
        name (str): Parameter can have only one name, so it **must** be a string
    '''

    def __repr__(self):  # pragma: no cover
        return "<Parameter name={}>".format(self.name)

    def __str__(self):  # pragma: no cover
        return "<Parameter  name={}>".format(self.name)

    def convert_to_argument(self):
        if not isinstance(self.name, str):
            raise TypeError("Inapropriate name type for Parameter. Should be a string")

        return super(Parameter, self).convert_to_argument()
