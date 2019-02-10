from shared.configuration.configuration_parser import Parser
import shared.configuration.interfaces.configuration as interfaces
import shared.configuration.implementations.configuration as impl
from shared.configuration.logging_configuration import create_logger, Logger, log_exception
from enum import Enum

class ConfigurationEnum(Enum):
    TelegramPusher = 0
    CommandAcceptor = 1
    CommandParser = 2


class ConfigurationFactory(object):

    @staticmethod
    def createConfiguration(directory: str, environment: str, configuration: ConfigurationEnum):
        create_logger("ConfigurationFactory").debug(
            f'{directory}/{environment}.ini')
        parser = Parser(f'{directory}/{environment}.ini')
        parser.parse()
        _return = None
        if configuration == ConfigurationEnum.TelegramPusher:
            _return = impl.TelegramPusherConfiguration(parser)
        return _return
