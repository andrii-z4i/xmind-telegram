from configparser import ConfigParser
from src.configuration.logging_configuration import create_logger, Logger, log_exception


class Parser(object):
    def __init__(self, file_name: str) -> None:
        self.logger: Logger = create_logger("Parser")
        self.logger.debug(f"in __init__({file_name})")
        self._file_name: str = file_name
        self._parser: ConfigParser = ConfigParser()

    def parse(self) -> None:
        self.logger.debug("in parse")
        if not self._file_name:
            self.logger.error("file name is empty")
            raise Exception('File name is empty')

        with open(self._file_name) as _file:
            self.logger.debug(f"read file {self._file_name}")
            self._parser.read_file(_file)

    def get_value(self, parameter: str) -> str:
        self.logger.debug(f"in get value for '{parameter}'")
        if '.' not in parameter:
            self.logger.debug("'.' is not in parameter")
            return self._parser[parameter]

        path = parameter.split('.')
        if len(path) > 2:
            self.logger.error('Path length has to be no longer than 2')
            raise Exception('Path length has to be no longer than 2')

        return self._parser[path[0]][path[1]]
