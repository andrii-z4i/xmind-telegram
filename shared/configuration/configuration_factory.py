from configuration.configuration_parser import Parser
import configuration.interfaces.configuration as interfaces
import configuration.implementations.configuration as impl
from configuration.logging_configuration import create_logger, Logger, log_exception


class ConfigurationFactory(object):

    @staticmethod
    def createConfiguration(directory: str, environment: str) -> interfaces.Configuration:
        create_logger("ConfigurationFactory").debug(
            f'{directory}/{environment}.ini')
        parser = Parser(f'{directory}/{environment}.ini')
        parser.parse()
        return impl.Configuration(parser)
