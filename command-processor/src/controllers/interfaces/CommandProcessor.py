from abc import ABC, abstractmethod
from model import SentMessage
from typing import List
from .ResponseContainer import ResponseContainer


class BaseCommand(ABC):

    @abstractmethod
    def create(self, user_id: str, title: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def select(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def list(self, user_id: str) -> ResponseContainer:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()


class CommandProcessor(ABC):

    @abstractmethod
    def process(self, message: SentMessage) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def file_commands(self) -> BaseCommand:
        raise NotImplementedError()

    @property
    @abstractmethod
    def node_commands(self) -> BaseCommand:
        raise NotImplementedError()

    @property
    @abstractmethod
    def topic_commands(self) -> BaseCommand:
        raise NotImplementedError()

    @property
    @abstractmethod
    def sheet_commands(self) -> BaseCommand:
        raise NotImplementedError()
