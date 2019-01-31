from abc import ABC, abstractmethod

class ServerConfiguration(ABC):
    @property
    @abstractmethod
    def host(self) -> str:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def port(self) -> int:
        raise NotImplementedError()


class QueueConfiguration(ServerConfiguration):
    @property
    @abstractmethod
    def queueName(self) -> str:
        raise NotImplementedError()


class TelegramConfiguration(ServerConfiguration):
    @property
    @abstractmethod
    def botKey(self) -> str:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def protocol(self) -> str:
        raise NotImplementedError()

class DatabaseConfiguration(ServerConfiguration):
    @property
    @abstractmethod
    def user(self) -> str:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def password(self) -> str:
        raise NotImplementedError()


class TelegramPusherConfiguration(ABC):
    @property
    @abstractmethod
    def queue(self) -> QueueConfiguration:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def telegram(self) -> TelegramConfiguration:
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def database(self) -> DatabaseConfiguration:
        raise NotImplementedError()