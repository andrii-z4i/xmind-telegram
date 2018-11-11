from typing import List
from abc import ABC, abstractmethod
from .ResponseContainer import ResponseContainer


class BaseCommandProcessor(ABC):

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

    @abstractmethod
    def current(self, user_id: str) -> str:
        raise NotImplementedError()
