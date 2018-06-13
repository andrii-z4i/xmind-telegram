from abc import ABC, abstractmethod
from app.models.ErrorMessage import ErrorMessage
from app.models.Command import Command


class CommandFactory(ABC):
    @abstractmethod
    def prepare_command(self) -> Command:
        raise NotImplementedError()
