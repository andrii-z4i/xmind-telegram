from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from ..interfaces.ResponseContainer import ResponseContainer
from src.file.user import UserObject
from src.file.operations.file import FileOperations


class FileCommandsProcessor(BaseCommandProcessor):
    """File commands"""

    def __init__(self, **kwargs):
        super(FileCommandsProcessor, self).__init__(kwargs)

    def create(self, user_id: str, title: str) -> bool:
        _user: UserObject = self._create_user_object(user_id)
        _file_operations: FileOperations = FileOperations(user_id)
        try:
            _file_operations.create(title)
        except:
            return False
        return True

    def select(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    def list(self, user_id: str) -> ResponseContainer:
        raise NotImplementedError()

    def delete(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    def _create_user_object(self, user_id: str) -> UserObject:
        _user: UserObject = UserObject(user_id)
        _user.working_dir = f'./working_dir/{user_id}'
        return _user
