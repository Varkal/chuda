import io
import shlex
import subprocess
import threading
import re
import signal
import os

NON_BLOCKING_ERROR_MESSAGE = "This method cannot be called on blocking shell commands"


class ShellCommand():

    def __init__(self, command, logger, cwd=None, block=True):
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
            self.output = self.process.stdout.read().decode("utf-8")
            self.error = self.process.stderr.read().decode("utf-8")
            self.return_code = self.process.returncode 

        return self

    def __create_process(self):
        self.process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            cwd=self.cwd
        )

    def run_non_blocking(self):
        if not self.block:
            self.__create_process()
            self.writer = io.TextIOWrapper(
                self.process.stdin,
                encoding='utf-8',
                line_buffering=True,  # send data on newline
            )
            any_lines = True
            while self.process.poll() is None or any_lines:
                any_lines = False
                stdout = self.process.stdout.readline()
                stderr = self.process.stderr.readline()
                if stdout:
                    any_lines = True
                    self.output.append(stdout.strip().decode("utf-8"))
                if stderr:
                    any_lines = True
                    self.error.append(stderr.strip().decode("utf-8"))
            self.return_code = self.process.poll()
            return self.process.poll()

        raise TypeError(NON_BLOCKING_ERROR_MESSAGE)

    def send(self, value):
        if not self.block:
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
                if len(self.output) > self.old_output_size:
                    while self.old_output_size < len(self.output):
                        self.logger.info(self.output[self.old_output_size])
                        self.old_output_size += 1

                if len(self.error) > self.old_error_size:
                    while self.old_error_size < len(self.error):
                        self.logger.error(self.error[self.old_error_size])
                        self.old_error_size += 1


class Runner():
    def __init__(self, logger=None, cwd=None):
        self.logger = logger
        self.cwd = cwd

    def run(self, command, block=True, cwd=None):
        if cwd is None:
            cwd = self.cwd

        return ShellCommand(command=command, logger=self.logger, block=block, cwd=cwd).run()
