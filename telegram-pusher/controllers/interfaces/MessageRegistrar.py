from abc import ABC, abstractmethod
from model import MessageContainer


class MessageRegistrar(ABC):

    @abstractmethod
    def store_message(self, message: MessageContainer) -> None:
        raise NotImplementedError()