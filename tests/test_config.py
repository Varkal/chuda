
import pytest
from chuda.app import App
from .utils import cli_args


TEST_STRING = "Test"


@pytest.mark.parametrize(
    "parser, path", [
        ["ini", ["/tmp/dontexist", "./tests/data/test_config.ini"]],
        ["ini", "./tests/data/test_config.ini"],
        ["json", ["./tests/data/test_config.json"]],
        ["yaml", ["./tests/data/test_config.yaml"]]
    ]
)
@cli_args(
    [TEST_STRING]
)
def test_config(argv, parser, path):
    class ConfigApp(App):
        config_parser = parser
        config_path = path

        def main(self):
            assert self.config["test"]["test_key"] == "test_value"

    app = ConfigApp()
    app.run()
