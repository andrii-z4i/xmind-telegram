import xmind
from src.file.user import UserObject
from src.file.operations.file import FileOperations
from src.file.metainformation import MetaInformation, MetaJsonInfo
from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from ..interfaces.ResponseContainer import ResponseContainer

class FileCommandsProcessor(BaseCommandProcessor):
    """File commands"""

    def __init__(self, **kwargs):
        super(FileCommandsProcessor, self).__init__()

    def create(self, user_id: str, title: str) -> bool:
        _user: UserObject = self.create_user_object(user_id)
        _file_operations: FileOperations = FileOperations(_user)
        try:
            _file_operations.create(title)
            _, _meta_json = self.read_meta_file(user_id)
            _current_file = _meta_json.current_file.file_name
            _xmind_workbook = xmind.load(self.get_full_file_path(user_id, \
                _current_file))
            _sheet = _xmind_workbook.getPrimarySheet()
            _sheet.setTitle('NewSheet')
            xmind.save(_xmind_workbook, self.get_full_file_path(user_id, \
                _current_file))
        except Exception as ex:
            print(ex)
            return False
        return True

    def select(self, user_id: str, virtual_index: int) -> bool:
        try:
            _meta_information, _meta_json = self.read_meta_file(user_id)
            _files = [file_name for file_name in
                      MetaInformation.enumerate_files(_meta_json)]
            _response_container = ResponseContainer(_files)
            _file_to_use = _response_container.get_title_by_index(virtual_index)
            _meta_information.change_current_file(_file_to_use)
        except:
            return False
        return True

    def list(self, user_id: str) -> ResponseContainer:
        _, _meta_json = self.read_meta_file(user_id)
        _files = [file_name for file_name in
                  MetaInformation.enumerate_files(_meta_json)]
        _response_container = ResponseContainer(_files)
        return _response_container


    def delete(self, user_id: str, virtual_index: int) -> bool:
        try:
            _meta_information, _meta_json = self.read_meta_file(user_id)
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
            _, _meta_json = self.read_meta_file(user_id)
            return _meta_json.current_file.file_name
        except:
            return None
