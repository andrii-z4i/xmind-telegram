from abc import ABC, abstractmethod


class QueueProcessor(ABC):

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError()
