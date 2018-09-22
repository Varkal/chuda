from chuda import App
from chuda.shell import ShellCommand
from .utils import cli_args
import logging
import time
from copy import copy
import pytest

logger = logging.getLogger("default")
logger.info = print


def test_basic_shell():
    ps = ShellCommand("echo 1", logger).run()
    assert ps.output == "1\n"


def test_async_shell():
    ps = ShellCommand("./tests/data/test.sh", logger, block=False).run()
    time.sleep(0.01)
    assert ps.is_running()
    ps.kill()


def test_write():
    ps = ShellCommand("./tests/data/test-write.sh", logger, block=False).run()
    time.sleep(0.01)
    ps.send("test")
    ps.poll_output()
    time.sleep(0.01)
    assert ps.output == ["test"]


def test_print_live_output(capsys):
    ps = ShellCommand("./tests/data/test.sh", logger, block=False).run()
    time.sleep(0.01)
    ps.print_live_output()
    stdout, _ = capsys.readouterr()
    assert stdout == "\n".join([str(x) for x in range(0, 5)])+"\n"


@pytest.mark.parametrize(
    "method, args", [
        ["run_non_blocking", []],
        ["send", ["test"]],
        ["kill", []],
        ["print_live_output", []]
    ]
)
def test_blocking_raise_exception(method, args):
    ps = ShellCommand("echo 1", logger).run()
    with pytest.raises(TypeError):
        getattr(ps, method)(*args)


@cli_args(
    ["test"]
)
def test_runner(argv, capsys):
    class ShellApp(App):
        def main(self):
            ps = self.shell.run("ls -1", cwd="./tests")
            self.logger.info(ps.output)

    ShellApp().run()
    stdout, _ = capsys.readouterr()
    assert "test_shell.py" in stdout.split("\n")
