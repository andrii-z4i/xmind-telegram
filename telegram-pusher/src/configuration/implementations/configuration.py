from typing import Any

import src.configuration.interfaces.configuration as interfaces
from src.configuration.configuration_parser import Parser


class Configuration(interfaces.Configuration):

    def __init__(self, parser: Parser) -> None:
        self._parser = parser

    def get_any_value(self, key) -> Any:
        if not self._parser:
            raise Exception('Parser is not set')

        return self._parser.get_value(key)

    def get_int_value(self, key) -> int:
        return int(self.get_any_value(key))

    def get_str_value(self, key):
        return str(self.get_any_value(key))

    @property
    def queueServer(self) -> str:
        return self.get_str_value('queue.queueServer')

    @property
    def queuePort(self) -> int:
        return self.get_int_value('queue.queuePort')

    @property
    def messagesQueueName(self) -> str:
        return self.get_str_value('queue.messagesQueueName')

    @property
    def errorsQueueName(self) -> str:
        return self.get_str_value('queue.errorsQueueName')

    @property
    def telegramProtocol(self) -> str:
        return self.get_str_value('telegram.protocol')

    @property
    def telegramPort(self) -> int:
        return self.get_int_value('telegram.port')

    @property
    def telegramBotKey(self) -> str:
        return self.get_str_value('telegram.botKey')

    @property
    def telegramHost(self) -> str:
        return self.get_str_value('telegram.host')

    @property
    def databaseHost(self) -> str:
        return self.get_str_value('database.host')

    @property
    def databaseName(self) -> str:
        return self.get_str_value('database.name')

    @property
    def databaseUser(self) -> str:
        return self.get_str_value('database.user')

    @property
    def databasePassword(self) -> str:
        return self.get_str_value('database.password')
