from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from ..interfaces.ResponseContainer import ResponseContainer
from src.file.user import UserObject
from src.file.operations.file import FileOperations
from src.file.metainformation import MetaInformation, MetaJsonInfo


class FileCommandsProcessor(BaseCommandProcessor):
    """File commands"""

    def __init__(self, **kwargs):
        super(FileCommandsProcessor, self).__init__()

    def create(self, user_id: str, title: str) -> bool:
        _user: UserObject = self._create_user_object(user_id)
        _file_operations: FileOperations = FileOperations(_user)
        try:
            _file_operations.create(title)
        except Exception as ex:
            print(ex)
            return False
        return True

    def select(self, user_id: str, virtual_index: int) -> bool:
        try:
            _meta_information, _meta_json = self._read_meta_file(user_id)
            _files = [file_name for file_name in
                      MetaInformation.enumerate_files(_meta_json)]
            _response_container = ResponseContainer(_files)
            _file_to_use = _response_container.get_title_by_index(virtual_index)
            _meta_information.change_current_file(_file_to_use)
        except:
            return False
        return True

    def list(self, user_id: str) -> ResponseContainer:
        _, _meta_json = self._read_meta_file(user_id)
        _files = [file_name for file_name in
                  MetaInformation.enumerate_files(_meta_json)]
        _response_container = ResponseContainer(_files)
        return _response_container


    def delete(self, user_id: str, virtual_index: int) -> bool:
        try:
            _meta_information, _meta_json = self._read_meta_file(user_id)
            _files = [file_name for file_name in
                      MetaInformation.enumerate_files(_meta_json)]
            _response_container = ResponseContainer(_files)
            _file_to_use = _response_container.get_title_by_index(virtual_index)
            _meta_information.remove_file(_file_to_use)
        except:
            return False
        return True

    def current(self, user_id: str) -> str:
        try:
            _, _meta_json = self._read_meta_file(user_id)
            return _meta_json.current_file.file_name
        except:
            return None

    def _create_user_object(self, user_id: str) -> UserObject:
        _user: UserObject = UserObject(user_id)
        _user.working_dir = f'./{user_id}'
        return _user

    def _read_meta_file(self, user_id: str) -> (MetaInformation, MetaJsonInfo):
        _user: UserObject = self._create_user_object(user_id)
        _meta_information: MetaInformation = MetaInformation(_user)
        _meta_json = _meta_information.read_meta_file()
        return _meta_information, _meta_json
