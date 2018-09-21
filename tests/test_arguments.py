from chuda import App, Parameter, Option
import pytest
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
    class InvalidArgApp(App):
        arguments = [param]

    with pytest.raises(TypeError):
        InvalidArgApp().run()

@pytest.mark.parametrize(
    "option", [
        Option("test_param"),
        Option(1),
        Option(-1),
        Option({}),
        Option(False),
        Option(True),
    ]
)
def test_type_options(option):
    class InvalidArgApp(App):
        arguments = [option]

    with pytest.raises(TypeError):
        InvalidArgApp().run()

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
