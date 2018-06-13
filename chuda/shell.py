import io
import shlex
import subprocess
import threading
import re
import signal
import os

NON_BLOCKING_ERROR_MESSAGE = "This method cannot be called on blocking shell commands"


class ShellCommand():

    def __init__(self, command, logger, cwd=None, block=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        self.command = shlex.split(command)
        self.block = block
        self.process = None
        self.thread = None
        self.output = None
        self.error = None
        self.old_output_size = 0
        self.old_error_size = 0
        self.logger = logger
        self.writer = None
        self.return_code = -1
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        if cwd:
            self.cwd = cwd.replace("~", os.getenv("HOME"))
        else:
            self.cwd = None

    def run(self):
        if not self.block:
            self.output = []
            self.error = []
            self.thread = threading.Thread(target=self.run_non_blocking)
            self.thread.start()
        else:
            self.__create_process()
            self.process.wait()
            if self._stdout is not None:
                self.output = self.process.stdout.read().decode("utf-8")
            if self._stderr is not None:
                self.error = self.process.stderr.read().decode("utf-8")
            self.return_code = self.process.returncode 

        return self

    def __create_process(self):
        self.process = subprocess.Popen(
            self.command,
            stdout=self._stdout,
            stderr=self._stderr,
            stdin=self._stdin,
            cwd=self.cwd
        )

    def run_non_blocking(self):
        if not self.block:
            self.__create_process()

            if self._stdin is not None:
                self.writer = io.TextIOWrapper(
                    self.process.stdin,
                    encoding='utf-8',
                    line_buffering=True,  # send data on newline
                )
            any_lines = True
            while self.process.poll() is None or any_lines:
                any_lines = False

                if self._stdout is not None:
                    stdout = self.process.stdout.readline()
                if self._stderr is not None:
                    stderr = self.process.stderr.readline()

                if self._stdout is not None and stdout:
                    any_lines = True
                    self.output.append(stdout.strip().decode("utf-8"))
                if self._stderr is not None and stderr:
                    any_lines = True
                    self.error.append(stderr.strip().decode("utf-8"))

            self.return_code = self.process.poll()
            return self.process.poll()

        raise TypeError(NON_BLOCKING_ERROR_MESSAGE)

    def send(self, value):
        if not self.block and self._stdin is not None:
            self.writer.write("{}\n".format(value))
        else:
            raise TypeError(NON_BLOCKING_ERROR_MESSAGE)

    def poll_output(self):
        if self.block:
            return self.output

        new_list = self.output[self.old_output_size:]
        self.old_output_size += len(new_list)
        return new_list

    def poll_error(self):
        if self.block:
            return self.error

        new_list = self.error[self.old_error_size:]
        self.old_error_size += len(new_list)
        return new_list

    def kill(self):
        if self.block:
            raise TypeError(NON_BLOCKING_ERROR_MESSAGE)

        try:
            self.process.kill()
        except ProcessLookupError as exc:
            self.logger.debug(exc)

    def wait_for(self, pattern, timeout=None):
        should_continue = True

        def stop(signum, frame):  # pylint: disable=W0613
            nonlocal should_continue
            if should_continue:
                raise TimeoutError()

        if timeout:
            signal.signal(signal.SIGALRM, stop)
            signal.alarm(timeout)

        while should_continue:
            output = self.poll_output() + self.poll_error()
            filtered = [line for line in output if re.match(pattern, line)]
            if filtered:
                should_continue = False

    def is_running(self):
        if self.block:
            return False

        return self.thread.is_alive() or self.process.poll() is None

    def wait(self):
        while self.is_running():
            pass

    def print_live_output(self):
        '''
        Blocking method
        '''
        if self.block:
            raise TypeError(NON_BLOCKING_ERROR_MESSAGE)
        else:
            while self.thread.is_alive() or self.old_output_size < len(self.output) or self.old_error_size < len(self.error):
                if self._stdout is not None and len(self.output) > self.old_output_size:
                    while self.old_output_size < len(self.output):
                        self.logger.info(self.output[self.old_output_size])
                        self.old_output_size += 1

                if self._stderr is not None and len(self.error) > self.old_error_size:
                    while self.old_error_size < len(self.error):
                        self.logger.error(self.error[self.old_error_size])
                        self.old_error_size += 1


class Runner():
    def __init__(self, logger=None, cwd=None):
        self.logger = logger
        self.cwd = cwd

    def run(self, command, block=True, cwd=None, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        if cwd is None:
            cwd = self.cwd

        return ShellCommand(command=command, logger=self.logger, block=block, cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr).run()
