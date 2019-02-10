from cmp_command_acceptor.app.acceptor_configuration.configuration_interface import Configuration


class ParsedConfiguration(Configuration):
    def __init__(self, parser):
        self._parser = parser

    @property
    def host(self):
        return self._parser.get_value('server.host')

    @property
    def port(self):
        return int(self._parser.get_value('server.port'))

    @property
    def debug(self):
        return bool(self._parser.get_value('server.debug'))

    @property
    def use_debugger(self):
        return bool(self._parser.get_value('server.use_debugger'))

    @property
    def use_reloader(self):
        return bool(self._parser.get_value('server.use_reloader'))

    @property
    def queuePort(self):
        return int(self._parser.get_value('queue.port'))

    @property
    def processorQueueName(self):
        return self._parser.get_value('queue.processorQueueName')

    @property
    def errorsQueueName(self):
        return self._parser.get_value('queue.errorsQueueName')

    @property
    def queueServer(self):
        return self._parser.get_value('queue.host')