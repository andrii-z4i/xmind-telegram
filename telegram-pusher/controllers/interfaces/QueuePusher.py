from abc import ABC, abstractmethod
from model import Message


class QueuePusher(ABC):

    @abstractmethod
    def put_message_to_queue(self, message: Message, retry_after: int) -> bool:
        raise NotImplementedError()