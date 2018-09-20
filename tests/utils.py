from unittest.mock import patch
from functools import wraps
import inspect

import pytest


def depth(list_):
    return isinstance(list_, list) and max(map(depth, list_))+1


def pipoargv(*args):
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


def new_argv(*args):
    def decorator(fun):
        def wrapper(*inner_args, **inner_kwargs):
            argv = inner_kwargs["argv"]
            if "argv" not in inspect.signature(fun).parameters:
                del inner_kwargs["argv"]
            with patch("sys.argv", argv):
                return fun(*inner_args, **inner_kwargs)

        wrapper = wraps(fun)(wrapper)
        # sig = inspect.signature(wrapper)
        # sig.replace(sig.parameters+inspect.Parameter())
        wrapper = pytest.mark.parametrize("argv", args)(wrapper)

        return wrapper


    return decorator
