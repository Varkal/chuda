from unittest.mock import patch
from functools import wraps


depth = lambda L: isinstance(L, list) and max(map(depth, L))+1

def argv(*args):
    arguments = list(args)
    def decorator(fun):        
        @wraps(fun)
        def wrapper(*args, **kwargs):
            if depth(arguments) == 1:
                with patch("sys.argv", arguments):
                    return fun(*args, **kwargs)
            else:
                for argument_list in arguments:
                    with patch("sys.argv", argument_list):
                        return fun(*args, **kwargs)
        return wrapper

    return decorator
