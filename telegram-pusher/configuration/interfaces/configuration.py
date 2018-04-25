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
    def messagesQueueName(self):
        return NotImplemented

    @property
    @abstractmethod
    def errorsQueueName(self):
        return NotImplemented