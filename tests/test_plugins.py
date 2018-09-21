from chuda import App, Plugin
from .utils import cli_args


class PluginTest(Plugin):
    def on_create(self):
        self.enrich_app("step_passed", [])
        self.app.step_passed.append("on_create")

    def on_signals_handled(self):
        self.app.step_passed.append("on_signals_handled")

    def on_config_read(self):
        self.app.step_passed.append("on_config_read")

    def on_arguments_parsed(self):
        self.app.step_passed.append("on_arguments_parsed")

    def on_logger_created(self):
        self.app.step_passed.append("on_logger_created")

    def on_run(self):
        self.app.step_passed.append("on_run")

    def on_end(self):
        self.app.step_passed.append("on_end")

    def custom_plugin_step(self):
        self.app.step_passed.append("custom_plugin_step")


class IncompletePlugin(Plugin):
    def on_create(self):
        self.app.step_passed.append("on_create 2")


class PluginApp(App):
    plugins = [
        PluginTest, IncompletePlugin()
    ]

    def main(self):
        self.call_plugins("custom_plugin_step")


@cli_args(["test"])
def test_plugins(argv):
    app = PluginApp()
    app.run()

    expected = [
        "on_create",  # PluginTest
        "on_create 2",  # IncompletePlugin
        "on_signals_handled",
        "on_config_read",
        "on_arguments_parsed",
        "on_logger_created",
        "on_run",
        "custom_plugin_step",
        "on_end",
    ]

    assert app.step_passed == expected  # pylint: disable=E1101
