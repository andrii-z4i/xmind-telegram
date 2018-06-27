from abc import ABC, abstractmethod
from model.AcceptedMessage import AcceptedMessage


class MessageHolder(ABC):

    @abstractmethod
    def put(self, message: AcceptedMessage)-> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> AcceptedMessage:
        raise NotImplementedError()

    @abstractmethod
    def isEmpty(self) -> bool:
        raise NotImplementedError()
    is_empty = isEmpty

