from abc import ABC, abstractmethod


class WorkspaceHandlerInterface(ABC):

    @abstractmethod
    def handle(self) -> bool:
        raise NotImplementedError()
