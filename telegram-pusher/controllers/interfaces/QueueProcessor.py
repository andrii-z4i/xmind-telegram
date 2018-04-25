from abc import ABC, abstractmethod


class QueueProcessor(ABC):

    @abstractmethod
    def register_callback(self, call_back_method) -> None:
        raise NotImplementedError()

    @abstractmethod
    def activate(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def deactivate(self) -> None:
        raise NotImplementedError()