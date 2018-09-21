from pathlib import Path
import pytest

from chuda import App, Parameter, Option
from .utils import cli_args


TEST_STRING = "test_value"


@cli_args(
    ["test_program", TEST_STRING],
    ["test_program", TEST_STRING, "--test-option", TEST_STRING],
    ["test_program", "1", "--test-option", "2"],
    ["test_program", "-1", "--test-option", "2"],
)
def test_basic_arguments(capsys, argv):
    class BasicArgsApp(App):
        arguments = [
            Parameter("test_param"),
            Option(["--test-option", "-T"])
        ]

        def main(self):
            self.logger.info(self.arguments.test_param)
            self.logger.info(self.arguments.test_option)

    app = BasicArgsApp()
    app.run()

    stdout, _ = capsys.readouterr()

    test_param = argv[1]
    test_option = None if len(argv) <= 3 else argv[3]

    assert stdout == "{}\n{}\n".format(test_param, test_option)


@pytest.mark.parametrize(
    "param", [
        Parameter(["test_param"]),
        Parameter(1),
        Parameter(-1),
        Parameter({}),
        Parameter(False),
        Parameter(True),
    ]
)
def test_type_params(param):
    class InvalidParamApp(App):
        arguments = [param]

    with pytest.raises(TypeError):
        InvalidParamApp().run()


@pytest.mark.parametrize(
    "option, exception_type", [
        [Option("test_param"), TypeError],
        [Option(1), TypeError],
        [Option(-1), TypeError],
        [Option({}), TypeError],
        [Option(False), TypeError],
        [Option(True), TypeError],
        [Option([]), ValueError],
    ]
)
def test_type_options(option, exception_type):
    class InvalidOptionApp(App):
        arguments = [option]

    with pytest.raises(exception_type):
        InvalidOptionApp().run()


@pytest.mark.parametrize(
    "option_names, expected", [
        [["--test"], "test"],
        [["-t"], "t"],
        [["-t", "--test"], "test"],
        [["-T"], "t"],
        [["--Test"], "test"],
        [["--TEST"], "test"],
        [["--TEST", "-T"], "test"],
        [["--test", "--pipo"], "test"],
        [["--pipo", "--test"], "pipo"],
    ]
)
def test_get_default_name(option_names, expected):
    assert Option(option_names).get_default_name() == expected


@cli_args(
    [TEST_STRING]
)
def test_path_values(capsys, argv):
    test_path = "/tmp/test"

    class PathApp(App):
        arguments = [
            Option(["--path"], default=Path(test_path))
        ]

        def main(self):
            self.logger.info(self.arguments.path)

    PathApp().run()

    stdout, _ = capsys.readouterr()
    assert stdout == "{}\n".format(test_path)
