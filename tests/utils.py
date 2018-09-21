from unittest.mock import patch
from functools import wraps
import inspect

import pytest

def cli_args(*args):
    def decorator(fun):
        if "argv" not in inspect.signature(fun).parameters:
            raise ValueError("Decorated methods with @cli_args must have a 'argv' parameter")

        @wraps(fun)
        @pytest.mark.parametrize("argv", args)
        def wrapper(*inner_args, **inner_kwargs):
            with patch("sys.argv", inner_kwargs["argv"]):
                return fun(*inner_args, **inner_kwargs)
        return wrapper

    return decorator
