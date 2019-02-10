from abc import ABC, abstractmethod
from shared.model.Message import Message
from shared.model.SentMessage import SentMessage


class MessageSender(ABC):

    @abstractmethod
    def send_message(self, message: Message) -> SentMessage:
        raise NotImplementedError()
