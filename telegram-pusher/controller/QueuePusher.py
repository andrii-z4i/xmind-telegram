from abc import ABCMeta, abstractmethod
from model import Message


class IQueuePusher(metaclass=ABCMeta):

    @abstractmethod
    def put_message_to_queue(self, message: Message, retry_after: int) -> bool:
        raise NotImplemented()
