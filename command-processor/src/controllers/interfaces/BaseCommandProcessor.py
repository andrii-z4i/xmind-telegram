from typing import List
from abc import ABC, abstractmethod
from src.file.user import UserObject
from src.file.metainformation import MetaInformation, MetaJsonInfo
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

    def create_user_object(self, user_id: str) -> UserObject:
        _user: UserObject = UserObject(user_id)
        _user.working_dir = f'./{user_id}'
        return _user

    def read_meta_file(self, user_id: str) -> (MetaInformation, MetaJsonInfo):
        _user: UserObject = self.create_user_object(user_id)
        _meta_information: MetaInformation = MetaInformation(_user)
        _meta_json = _meta_information.read_meta_file()
        return _meta_information, _meta_json

    def get_full_file_path(self, user_id: str, file_name: str) -> str:
        _user_object: UserObject = self.create_user_object(user_id)
        return f"{_user_object.working_dir}/{file_name}"

