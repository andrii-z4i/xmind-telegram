from typing import Any

import shared.configuration.interfaces.configuration as interfaces
from shared.configuration.configuration_parser import Parser
from shared.configuration.logging_configuration import create_logger, Logger, log_exception


class ServerConfiguration(interfaces.ServerConfiguration):

    def __init__(self, parser: Parser, section: str) -> None:
        self.logger: Logger = create_logger("Configuration")
        self.logger.debug("in __init__")
        self._parser = parser
        self._section = section

    def get_any_value(self, key) -> Any:
        self.logger.debug(f"in get any value for {key}")
        if not self._parser:
            self.logger.error("Parser is not set")
            raise Exception('Parser is not set')
        value = self._parser.get_value(self._section, key)
        self.logger.debug(f"got value {value}")
        return value

    def get_int_value(self, key) -> int:
        return int(self.get_any_value(key))

    def get_str_value(self, key):
        return str(self.get_any_value(key))

    @property
    def host(self) -> str:
        return self.get_str_value('server')
    
    @property
    def port(self) -> int:
        return self.get_int_value('port')


class QueueConfiguration(ServerConfiguration, interfaces.QueueConfiguration):
    @property
    def queueName(self) -> str:
        return self.get_str_value('queueName')


class TelegramConfiguration(ServerConfiguration, interfaces.TelegramConfiguration):
    @property
    def botKey(self) -> str:
        return self.get_str_value('botKey')
    
    @property
    def protocol(self) -> str:
        return self.get_str_value('protocol')


class DatabaseConfiguration(ServerConfiguration, interfaces.DatabaseConfiguration):
    @property
    def user(self) -> str:
        return self.get_str_value('user')
    
    @property
    def password(self) -> str:
        return self.get_str_value('password')


class TelegramPusherConfiguration(interfaces.TelegramPusherConfiguration):
    
    def __init__(self, parser: Parser) -> None:
        self.logger: Logger = create_logger("Configuration")
        self.logger.debug("in __init__")
        self._parser = parser
        self._queue = QueueConfiguration(parser, 'queue')
        self._telegram = TelegramConfiguration(parser, 'telegram')
        self._database = DatabaseConfiguration(parser, 'database')

    @property
    def queue(self) -> interfaces.QueueConfiguration:
        return self._queue
    
    @property
    def telegram(self) -> interfaces.TelegramConfiguration:
        return self._telegram
    
    @property
    def database(self) -> DatabaseConfiguration:
        return self._database