from configuration.configuration_parser import Parser
import configuration.interfaces.configuration as interfaces
import configuration.implementations.configuration as impl


class ConfigurationFactory(object):

    @staticmethod
    def createConfiguration(directory: str, environment: str) -> interfaces.Configuration:
        parser = Parser(f'./{directory}/{environment}.ini')
        parser.parse()
        return impl.Configuration(parser)