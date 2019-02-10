import xmind
from cmp_command_processor.src.controllers.interfaces.BaseCommandProcessor import BaseCommandProcessor
from cmp_command_processor.src.controllers.interfaces.ResponseContainer import ResponseContainer


class SheetCommandsProcessor(BaseCommandProcessor):
    """Sheet commands"""

    def __init__(self, **kwargs):
        super(SheetCommandsProcessor, self).__init__()

    def create(self, user_id: str, title: str) -> bool:
        try:
            _xmind_workbook, _current_file = self.get_workbook(user_id)
            _new_sheet = _xmind_workbook.createSheet()
            _new_sheet.setTitle(title)
            _xmind_workbook.addSheet(_new_sheet)
            xmind.save(_xmind_workbook, self.get_full_file_path(user_id, \
                _current_file))
            return True
        except:
            return False

    def select(self, user_id: str, virtual_index: int) -> bool:
        try:
            _xmind_workbook, _current_file = self.get_workbook(user_id)
            _sheets = [sheet.getTitle() for sheet in _xmind_workbook.getSheets()]
            _response_container = ResponseContainer(_sheets)
            _sheet_to_use = \
                _response_container.get_title_by_index(virtual_index)
            _old_index = _sheets.index(_sheet_to_use)
            _xmind_workbook.moveSheet(_old_index, 0)
            xmind.save(_xmind_workbook, self.get_full_file_path(user_id, \
                _current_file))
            return True
        except:
            return False

    def list(self, user_id: str) -> ResponseContainer:
        _xmind_workbook, _ = self.get_workbook(user_id)
        _sheets = [sheet.getTitle() for sheet in _xmind_workbook.getSheets()]
        _response_container = ResponseContainer(_sheets)
        return _response_container

    def delete(self, user_id: str, virtual_index: int) -> bool:
        try:
            _xmind_workbook, _current_file = self.get_workbook(user_id)
            _sheets = [sheet.getTitle() for sheet in _xmind_workbook.getSheets()]
            _response_container = ResponseContainer(_sheets)
            _sheet_to_use = \
                _response_container.get_title_by_index(virtual_index)
            _old_index = _sheets.index(_sheet_to_use)
            _xmind_workbook.removeSheet(_xmind_workbook.getSheets()[_old_index])
            xmind.save(_xmind_workbook, self.get_full_file_path(user_id, \
                _current_file))
            return True
        except:
            return False

    def current(self, user_id: str) -> str:
        try:
            _xmind_workbook, _ = self.get_workbook(user_id)
            return _xmind_workbook.getPrimarySheet().getTitle()
        except:
            return None

    def get_workbook(self, user_id: str) -> \
        (xmind.core.workbook.WorkbookDocument, str):
        _, _meta_json = self.read_meta_file(user_id)
        _current_file = _meta_json.current_file.file_name
        _xmind_workbook = xmind.load(self.get_full_file_path(user_id, \
                _current_file))
        return _xmind_workbook, _current_file
