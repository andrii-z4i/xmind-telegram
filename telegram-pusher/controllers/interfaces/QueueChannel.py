
from abc import ABC, abstractmethod
from typing import Callable


class QueueChannel(ABC):

    def __init__(self):
        super().__init__()
        self._callback: Callable[[str, str, str, str], None] = None

    def set_callback_method(self, callback: Callable[[str, str, str, str], None]) -> None:
        self._callback = callback

    @abstractmethod
    def activate_consumer(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def start_consuming(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def stop_consuming(self) -> None:
        raise NotImplementedError()
