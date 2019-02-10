
from abc import ABC, abstractmethod
from typing import Callable


class QueueChannelInterface(ABC):

    @abstractmethod
    def declare_queue(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def activate_consumer(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def deactivate_consumer(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_inner_message_processor(self, callback: Callable[[dict], None]) -> None:
        raise NotImplementedError()
