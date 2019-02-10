from abc import ABC, abstractmethod
from shared.model import MessageContainer


class MessageRegistrar(ABC):

    @abstractmethod
    def store_message(self, message_body: str) -> None:
        raise NotImplementedError()