from chuda import App, Parameter, Option
from .utils import argv

TEST_STRING = "test_value"

@argv("test_program", TEST_STRING)
def test_basic_arguments(capsys):
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
    assert stdout == TEST_STRING+"\nNone\n"
