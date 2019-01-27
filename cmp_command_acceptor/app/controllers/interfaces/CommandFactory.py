from abc import ABC, abstractmethod
from shared.model.Command import Command


class CommandFactory(ABC):
    @abstractmethod
    def prepare_command(self) -> Command:
        raise NotImplementedError()
