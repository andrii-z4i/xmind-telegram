from abc import ABC, abstractmethod
from model import SentMessage
from typing import List
from .ResponseContainer import ResponseContainer
from .BaseCommandProcessor import BaseCommandProcessor


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
