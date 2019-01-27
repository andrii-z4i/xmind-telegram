from abc import ABC, abstractmethod
from shared.model.AcceptedMessage import AcceptedMessage


class RequestAnalyser(ABC):
    @property
    @abstractmethod
    def process(self) -> AcceptedMessage:
        raise NotImplementedError()

    # @abstractmethod
    # def accepted_message(self) -> AcceptedMessage:
    #     raise NotImplementedError()
