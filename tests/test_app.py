from chuda.app import App
from .utils import argv


TEST_STRING = "Test"


class BasicApp(App):
    app_name = "basic_app"

    def main(self):
        self.logger.debug(TEST_STRING)
        self.logger.info(TEST_STRING)


def test_run_call_main(mocker):
    app = BasicApp()
    mocker.spy(app, "main")
    app.run()
    assert getattr(app.main, "call_count") == 1


def test_output(capsys):
    app = BasicApp()
    app.run()
    stdout, _ = capsys.readouterr()
    assert stdout == TEST_STRING+"\n"


@argv(
    [TEST_STRING, "--quiet"],
    [TEST_STRING, "-q"]
)
def test_quiet(capsys):
    app = BasicApp()
    app.run()
    stdout, _ = capsys.readouterr()
    assert stdout == ""


@argv(TEST_STRING, "--version")
def test_version(capsys):
    app = BasicApp()
    app.run()
    stdout, _ = capsys.readouterr()
    assert stdout == "{}: {}\n".format(app.app_name, app.version)


@argv(
    [TEST_STRING, "--verbose"],
    [TEST_STRING, "-v"]
)
def test_verbose(capsys):
    app = BasicApp()
    app.run()
    stdout, _ = capsys.readouterr()
    assert stdout == "{}\n{}\n".format(TEST_STRING, TEST_STRING)


@argv(
    [TEST_STRING, "--help"],
    [TEST_STRING, "-h"]
)
def test_help(mocker):
    app = BasicApp()
    mocker.spy(app.parser, "print_help")
    app.run()
    assert getattr(app.parser.print_help, "call_count") == 1
