import xmind
from xmind.core.topic import TopicElement, TopicsElement
from xmind.core import const
from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from ..interfaces.ResponseContainer import ResponseContainer


class TopicCommandsProcessor(BaseCommandProcessor):
    """Topic commands"""

    def __init__(self, **kwargs):
        super(TopicCommandsProcessor).__init__()

    def create(self, user_id: str, title: str) -> bool:
        try:
            _sheet, _wb, _current_file = self.get_sheet(user_id)
            _new_topic = TopicElement(ownerWorkbook=_wb)
            _new_topic.setTitle(title)
            _sheet.appendChild(_new_topic)
            xmind.save(_wb, self.get_full_file_path(user_id, \
                _current_file))
            return True
        except:
            return False

    def select(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    def list(self, user_id: str) -> ResponseContainer:
        import ipdb
        ipdb.set_trace()
        _sheet, _wb, _current_file = self.get_sheet(user_id)
        _topics_element = _sheet.getChildNodesByTagName(const.TAG_TOPIC)
         # TopicsElement(ownerWorkbook=_wb)
        _topics = _topics_element.getSubTopics()
        _topics = [topic.getTitle() for topic in _topics]
        _response_container = ResponseContainer(_topics)
        return _response_container

    def delete(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    def current(self, user_id: str) -> str:
        raise NotImplementedError()

    def get_sheet(self, user_id: str) -> \
        (xmind.core.sheet.SheetElement, xmind.core.workbook.WorkbookDocument, str):
        _, _meta_json = self.read_meta_file(user_id)
        _current_file = _meta_json.current_file.file_name
        _xmind_workbook = xmind.load(self.get_full_file_path(user_id, \
                _current_file))
        _sheet = _xmind_workbook.getPrimarySheet()
        return _sheet, _xmind_workbook, _current_file
