class ChudaException(Exception):
    pass

class EmptyCommandNameException(ChudaException):
    message = "The command_name attribute is required and cannot be empty"

class ArgumentNotFoundException(ChudaException):
    message = "Argument {} not found"

    def __init__(self, arg_name):
        super().__init__(self.message.format(arg_name))
