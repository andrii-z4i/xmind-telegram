from abc import ABC, abstractmethod


class Configuration(ABC):
    @property
    @abstractmethod
    def queueServer(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def queuePort(self) -> int:
        return NotImplemented

    @property
    @abstractmethod
    def messagesQueueName(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def errorsQueueName(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def telegramProtocol(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def telegramPort(self) -> int:
        return NotImplemented

    @property
    @abstractmethod
    def telegramBotKey(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def telegramHost(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def databaseHost(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def databaseName(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def databaseUser(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def databasePassword(self) -> str:
        return NotImplemented