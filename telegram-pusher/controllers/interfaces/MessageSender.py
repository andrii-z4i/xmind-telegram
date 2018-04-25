from abc import ABC, abstractmethod
from model.Message import Message
from model.SentMessage import SentMessage


class MessageSender(ABC):

    @abstractmethod
    def send_message(self, message: Message) -> SentMessage:
        raise NotImplementedError()
