from configparser import ConfigParser
from shared.configuration.logging_configuration import create_logger, Logger, log_exception


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

    def get_value(self, section: str, parameter: str = None) -> str:
        self.logger.debug(f"in get value for '{parameter}'")
        if not parameter:
            self.logger.debug("parameter wasn't passed")
            _parts = section.split('.')
            if len(_parts) != 2:
                raise Exception("Path length has to be no longer than 2")
            else:
                return self._parser.get(_parts[0], _parts[1])
        
        if not parameter:
            self.logger.error("parameter is empty")
            raise Exception("Parameter wasn't passed")
        

        return self._parser.get(section, parameter)
