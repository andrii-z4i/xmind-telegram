from app.configuration.configuration_parser import Parser
from app.configuration.parsed_configuration import ParsedConfiguration


class ConfigurationFactory(object):

    @staticmethod
    def createConfiguration(environment):
        parser = Parser('./configuration/%s.ini' % environment)
        parser.parse()
        return ParsedConfiguration(parser)
        