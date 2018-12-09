import xmind
from xmind.core.topic import TopicElement, TopicsElement
from xmind.core import const
from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from ..interfaces.ResponseContainer import ResponseContainer
from src.file.metainformation import PathItem, MetaFileObject


class TopicCommandsProcessor(BaseCommandProcessor):
    """Topic commands"""

    def create(self, user_id: str, title: str) -> bool:
        try:
            _path, _sheet, _wb, _current_file = self.get_sheet(user_id)
            # here we need to get to the element by path
            _topic_element = self.get_topic_by_path(_sheet, _path)
            _new_topic = TopicElement(ownerWorkbook=_wb)
            _new_topic.setTitle(title)
            _topic_element.addSubTopic(_new_topic)
            xmind.save(_wb, self.get_full_file_path(user_id, \
                _current_file))
            return True
        except Exception as _ex:
            print(_ex)
            return False

    def select(self, user_id: str, virtual_index: int) -> bool:
        # virtual_index == -1 should navigate up
        raise NotImplementedError()

    def list(self, user_id: str) -> ResponseContainer:
        _path_item, _sheet, _wb, _current_file = self.get_sheet(user_id)
        _topic_element = self.get_topic_by_path(_sheet, _path_item)
        _topics = _topic_element.getSubTopics()
        _topics = [topic.getTitle() for topic in _topics]
        _response_container = ResponseContainer(_topics)
        return _response_container

    def delete(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    def current(self, user_id: str) -> str:
        raise NotImplementedError()

    def get_sheet(self, user_id: str) -> \
        (PathItem, xmind.core.sheet.SheetElement, xmind.core.workbook.WorkbookDocument, str):
        _, _meta_json = self.read_meta_file(user_id)
        _current_file = _meta_json.current_file.file_name
        _current_sheet = _meta_json.current_file.current_sheet
        _xmind_workbook = xmind.load(self.get_full_file_path(user_id, \
                _current_file))
        _sheet = _xmind_workbook.getSheets()[_current_sheet]
        _path_item = self.get_path_item_by_sheet_index(_current_sheet, \
                _meta_json.current_file)
        return _path_item, _sheet, _xmind_workbook, _current_file

    def get_path_item_by_sheet_index(self, sheet_index: int, \
            meta_file_object: MetaFileObject) -> PathItem:
        for ctx in meta_file_object.context:
            if ctx.sheet_index == sheet_index:
                return ctx
        return None

    def get_topic_by_path(self, sheet: xmind.core.sheet.SheetElement, path: \
            PathItem) -> TopicElement:
        _root_topic = sheet.getRootTopic()
        return _root_topic
