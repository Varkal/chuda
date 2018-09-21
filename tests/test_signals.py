from chuda import App, signal_handler
from .utils import cli_args
import time
import signal
import sys
import os
import pytest


@cli_args(["test"])
def test_signal(argv):
    class SignalApp(App):
        @signal_handler(signal.SIGINT)
        def handle_ctrl_c(self, signum, frame):  # pylint: disable=W0613
            self.logger.info("ctrl_c")
            sys.exit(2)

        def main(self):
            pass

    app = SignalApp()
    app.run()

    with pytest.raises(SystemExit):
        os.kill(os.getpid(), signal.SIGINT)
