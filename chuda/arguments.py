from .utils import to_snake_case

'''
Module with argparse utils for chuda
'''


class Argument:
    '''
    Abstract parent class for Option and Parameter
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
    completer = None

    def __init__(self, name=None, action="store", nargs=None, const=None,
                 default=None, type=None, choices=None, required=None, help=None, # pylint: disable=W0622
                 metavar=None, dest=None, completer=None):
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
    Represent an option on the command-line (--whatever)
    '''

    def __repr__(self):
        return "<Option name={}>".format(self.name)

    def __str__(self):
        return "<Option name={}>".format(self.name)

    def get_default_name(self):
        long_names = [name for name in self.name if name.startswith("--")]
        short_names = [name for name in self.name if not name.startswith("--")]

        if long_names:
            return to_snake_case(long_names[0].lstrip("-"))

        return to_snake_case(short_names[0])

    def convert_to_argument(self):
        if not isinstance(self.name, list) and not isinstance(self.name, tuple):
            raise TypeError("Inapropriate name type for Option. Should be a tuple or a list")

        if not self.name:
            raise ValueError("Name list cannot be empty")

        return super(Option, self).convert_to_argument()


class Parameter(Argument):
    '''
    Represent a parameter on the command-line (macommand whatever)
    '''

    def __repr__(self):
        return "<Parameter name={}>".format(self.name)

    def __str__(self):
        return "<Parameter  name={}>".format(self.name)

    def convert_to_argument(self):
        if not isinstance(self.name, str):
            raise TypeError("Inapropriate name type for Parameter. Should be a string")

        return super(Parameter, self).convert_to_argument()
