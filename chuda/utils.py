'''
Utils for Chuda internals
'''

import collections
import logging
import re

DEFAULT_LOGGER_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": '%(message)s'
        },
        "date": {
            "format": '%(asctime)s - %(levelname)s - %(message)s',
            "datefmt": '%Y-%m-%d %H:%M:%S'
        }
    },
    "handlers": {
        "console": {
            "class": "chuda.logging.ColoredStreamHandler",
            "formatter": "default",
            "level": "INFO",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "default": {
            "handlers": ["console"],
            "level": "INFO"
        }
    }
}


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, _ in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def get_flag(base, attr):
    return getattr(base, attr, False)


def isset(var, scope=globals):
    return var in scope()


class Null(object):

    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Null, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "<Null>"

    def __str__(self):
        return ""

    def __eq__(self, other):
        return id(self) == id(other) or other is None

    __nonzero__ = __bool__ = lambda self: False

    nullify = lambda self, *x, **kwargs: self

    __call__ = nullify
    __getattr__ = __setattr__ = __delattr__ = nullify
    __cmp__ = __ne__ = __lt__ = __gt__ = __le__ = __ge__ = nullify
    __pos__ = __neg__ = __abs__ = __invert__ = nullify
    __add__ = __sub__ = __mul__ = __mod__ = __pow__ = nullify
    __floordiv__ = __div__ = __truediv__ = __divmod__ = nullify
    __lshift__ = __rshift__ = __and__ = __or__ = __xor__ = nullify
    __radd__ = __rsub__ = __rmul__ = __rmod__ = __rpow__ = nullify
    __rfloordiv__ = __rdiv__ = __rtruediv__ = __rdivmod__ = nullify
    __rlshift__ = __rrshift__ = __rand__ = __ror__ = __rxor__ = nullify
    __iadd__ = __isub__ = __imul__ = __imod__ = __ipow__ = nullify
    __ifloordiv__ = __idiv__ = __itruediv__ = __idivmod__ = nullify
    __ilshift__ = __irshift__ = __iand__ = __ior__ = __ixor__ = nullify
    __getitem__ = __setitem__ = __delitem__ = nullify
    __getslice__ = __setslice__ = __delslice__ = nullify
    __reversed__ = nullify
    __contains__ = __missing__ = nullify
    __enter__ = __exit__ = nullify


def to_snake_case(name):
    s_1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s_1 = s_1.replace("-", "_")
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s_1).lower()


class LoggerMixin():

    @property
    def logger(self):
        logger_name = getattr(self, "logger_name", "default")
        return logging.getLogger(logger_name)
