from chuda.shell import ShellCommand
from .utils import cli_args
import logging
import time
from copy import copy

logger = logging.getLogger("default")


def test_basic_shell():
    ps = ShellCommand("echo 1", logger).run()
    assert ps.output == "1\n"


def test_async_shell():
    ps = ShellCommand("./tests/data/test.sh", logger, block=False).run()
    time.sleep(1)
    assert ps.is_running()
    ps.kill()
