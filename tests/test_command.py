
import re
import pytest
from chuda import App, Command, Parameter, Option
from .utils import cli_args


TEST_STRING = "Test"
COMMAND_NAMES = ["test-command", "other-test-command"]


@cli_args(
    [TEST_STRING, COMMAND_NAMES[0]],
    [TEST_STRING, COMMAND_NAMES[1]]
)
def test_command(argv, capsys):
    class TestCommand(Command):
        command_name = COMMAND_NAMES[0]
        description = TEST_STRING

        def main(self):
            self.logger.info(self.command_name)

    class OtherTestCommand(Command):
        command_name = COMMAND_NAMES[1]
        description = TEST_STRING

        def main(self):
            self.logger.info(self.command_name)

    class CommandApp(App):
        app_name = TEST_STRING
        description = TEST_STRING

        subcommands = [
            TestCommand, OtherTestCommand
        ]

    app = CommandApp()
    app.run()

    stdout, _ = capsys.readouterr()
    assert stdout == "{}\n".format(argv[1])


@cli_args(
    [TEST_STRING, COMMAND_NAMES[0], TEST_STRING],
    [TEST_STRING, COMMAND_NAMES[0], TEST_STRING, "--test-option", TEST_STRING],
    [TEST_STRING, COMMAND_NAMES[0], TEST_STRING, "--test-option", TEST_STRING, "--parent-option", TEST_STRING],
)
def test_arguments_command(argv, capsys):
    class TestCommand(Command):
        command_name = COMMAND_NAMES[0]
        description = TEST_STRING

        arguments = [
            Parameter("test_param"),
            Option(["--test-option"]),
        ]

        def main(self):
            self.logger.info(self.arguments.test_param)
            self.logger.info(self.arguments.test_option)
            self.logger.info(self.arguments.parent_option)

    class CommandApp(App):
        app_name = TEST_STRING
        description = TEST_STRING

        arguments = [
            Option(["--parent-option"]),
        ]

        subcommands = [
            TestCommand
        ]

    app = CommandApp()
    app.run()

    test_param = argv[2]
    test_option = None if len(argv) < 4 else argv[4]
    parent_option = None if len(argv) < 6 else argv[6]

    stdout, _ = capsys.readouterr()
    assert stdout == "{}\n{}\n{}\n".format(test_param, test_option, parent_option)


@cli_args(
    [TEST_STRING, COMMAND_NAMES[1]],
)
def test_call_other_command(argv, capsys):
    class TestCommand(Command):
        command_name = COMMAND_NAMES[0]
        description = TEST_STRING

        arguments = [
            Parameter("test_param"),
            Option(["--test-option"], required=True),
        ]

        def main(self):
            self.logger.info(self.arguments.test_param)
            self.logger.info(self.arguments.test_option)
            self.logger.info(self.arguments.parent_option)

    class OtherTestCommand(Command):
        command_name = COMMAND_NAMES[1]
        description = TEST_STRING

        def main(self):
            self.app.subcommands[COMMAND_NAMES[0]].run()

    class CommandApp(App):
        app_name = TEST_STRING
        description = TEST_STRING

        arguments = [
            Option(["--parent-option"]),
        ]

        subcommands = [
            TestCommand, OtherTestCommand
        ]

    app = CommandApp()
    app.run()

    stdout, _ = capsys.readouterr()
    assert re.match(".*Cannot run.*", stdout)  # TODO _check_arguments should raise an exception instead of logging


@cli_args([TEST_STRING])
def test_command_must_have_name(argv):
    class NoNameCommand(Command):
        description = TEST_STRING

    class NoNameApp(App):
        subcommands = [
            NoNameCommand
        ]

    with pytest.raises(SystemExit):
        NoNameApp().run()  # TODO should raise an exception instead of logging and exit


@cli_args(
    [TEST_STRING, COMMAND_NAMES[0]],
    [TEST_STRING]
)
def test_subconfig(argv):
    class SubConfigCommand(Command):
        command_name = COMMAND_NAMES[0]
        description = TEST_STRING
        use_subconfig = True
        config_path = "./tests/data/test_subconfig.ini"

        def main(self):
            assert self.config["subtest"]["subtest_key"] == "subtest_value"

    class SubConfigApp(App):
        subcommands = [
            SubConfigCommand
        ]

        config_path = "./tests/data/test_config.ini"

        def main(self):
            assert self.config["test"]["test_key"] == "test_value"

    SubConfigApp().run()
