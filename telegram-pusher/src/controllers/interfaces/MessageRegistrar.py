from abc import ABC, abstractmethod
from src.model import MessageContainer


class MessageRegistrar(ABC):

    @abstractmethod
    def store_message(self, message: MessageContainer) -> None:
        raise NotImplementedError()