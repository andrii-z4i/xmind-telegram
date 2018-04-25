import configuration.interfaces.configuration as interfaces


class Configuration(interfaces.Configuration):

    def __init__(self, parser):
        self._parser = parser

    @property
    def queueServer(self) -> str:
        return self._parser.get_value('server.queueServer')

    @property
    def queuePort(self) -> int:
        return int(self._parser.get_value('server.queuePort'))

    @property
    def messagesQueueName(self) -> str:
        return self._parser.get_value('server.messagesQueueName')

    @property
    def errorsQueueName(self) -> str:
        return self._parser.get_value('server.errorsQueueName')
