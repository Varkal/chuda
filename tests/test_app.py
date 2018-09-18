from chuda.app import App


TEST_STRING = "Test"


class BasicApp(App):
    def main(self):
        self.logger.info(TEST_STRING)


def test_run_call_main(mocker):
    app = BasicApp()
    mocker.spy(app, "main")
    app.run()
    assert getattr(app.main, "call_count") == 1


def test_output(capsys):
    app = BasicApp()
    app.run()
    stdout = capsys.readouterr()[0]
    assert stdout == TEST_STRING+"\n"
