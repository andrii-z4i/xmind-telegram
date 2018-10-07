from abc import ABC, abstractmethod


class FileHandlerInterface(ABC):

    @abstractmethod
    def handle(self) -> bool:
        raise NotImplementedError()
