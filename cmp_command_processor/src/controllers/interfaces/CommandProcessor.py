from abc import ABC, abstractmethod
from shared.model import SentMessage
from typing import List
from cmp_command_processor.src.controllers.interfaces.ResponseContainer import ResponseContainer
from cmp_command_processor.src.controllers.interfaces.BaseCommandProcessor import BaseCommandProcessor


class CommandProcessor(ABC):

    @abstractmethod
    def process(self, message: SentMessage) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def file_commands(self) -> BaseCommandProcessor:
        raise NotImplementedError()

    @property
    @abstractmethod
    def topic_commands(self) -> BaseCommandProcessor:
        raise NotImplementedError()

    @property
    @abstractmethod
    def sheet_commands(self) -> BaseCommandProcessor:
        raise NotImplementedError()
