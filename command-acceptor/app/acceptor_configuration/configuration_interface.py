from abc import ABC, abstractmethod


class Configuration(ABC):
    @property
    @abstractmethod
    def queueServer(self):
        return NotImplemented

    @property
    @abstractmethod
    def queuePort(self):
        return NotImplemented

    @property
    @abstractmethod
    def processorQueueName(self):
        return NotImplemented

    @property
    @abstractmethod
    def errorsQueueName(self):
        return NotImplemented

    @property
    @abstractmethod
    def host(self):
        return NotImplemented

    @property
    @abstractmethod
    def port(self):
        return NotImplemented

    @property
    @abstractmethod
    def debug(self):
        return NotImplemented

    @property
    @abstractmethod
    def use_debugger(self):
        return NotImplemented

    @property
    @abstractmethod
    def use_reloader(self):
        return NotImplemented
