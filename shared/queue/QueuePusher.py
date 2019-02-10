from abc import ABC, abstractmethod
from shared.model import MessageContainer


class QueuePusher(ABC):

    @abstractmethod
    def put_message_to_queue(self, message: MessageContainer, retry_after: int) -> bool:
        raise NotImplementedError()