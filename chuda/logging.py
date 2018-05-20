from logging import StreamHandler
import crayons

class ColoredStreamHandler(StreamHandler):
    colours = {
        'DEBUG': crayons.cyan,
        'WARN': crayons.yellow,
        'WARNING': crayons.yellow,
        'ERROR': crayons.red,
        'CRIT': lambda m: crayons.red(m, bold=True),
        'CRITICAL': lambda m: crayons.red(m, bold=True),
    }


    def emit(self, record):
        try:
            message = self.format(record)
            if self.colours.get(record.levelname, None):
                self.stream.write("{}".format(self.colours[record.levelname](message)))
            else:
                self.stream.write(message)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except: # pylint: disable=W0702
            self.handleError(record)
