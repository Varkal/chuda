
from chuda import autorun
from collections import namedtuple
from types import SimpleNamespace


class Dummy:
    def run(self):
        print("test")


def fake_get_module(cls):
    return SimpleNamespace(__name__="__main__")


def test_autorun(mocker, capsys):
    mocker.patch("inspect.getmodule", fake_get_module)
    autorun()(Dummy)
    stdout, _ = capsys.readouterr()
    assert stdout == "test\n"
