from abc import ABC, abstractmethod
from src.model.Message import Message
from src.model.SentMessage import SentMessage


class MessageSender(ABC):

    @abstractmethod
    def send_message(self, message: Message) -> SentMessage:
        raise NotImplementedError()
