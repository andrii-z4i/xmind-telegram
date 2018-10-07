from abc import ABC, abstractmethod
from model import SentMessage


class CommandProcessor(ABC):

    @abstractmethod
    def process(self, message: SentMessage) -> bool:
        raise NotImplementedError()
