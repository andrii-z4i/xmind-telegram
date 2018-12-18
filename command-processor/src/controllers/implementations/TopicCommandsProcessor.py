import xmind
from xmind.core.topic import TopicElement, TopicsElement
from xmind.core import const
from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from ..interfaces.ResponseContainer import ResponseContainer
from src.file.metainformation import PathItem, MetaFileObject
from typing import List


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
                _current_file.file_name))
            return True
        except Exception as _ex:
            print(_ex)
            return False

    def select(self, user_id: str, virtual_index: int) -> bool:
        _response_container: ResponseContainer = self.list(user_id)
        if virtual_index == -1:
            # go up
            raise NotImplementedError()
        try:
            _response_container.get_title_by_index(virtual_index)
        except Exception as _ex:
            return False
        
        _, _, _, _current_file = self.get_sheet(user_id)
        _path_item = _current_file.context
        _path_item.append(PathItem(step=len(_path_item), v_index=virtual_index, sheet_index=_current_file.current_sheet))
        
        _meta_information, _ = self.read_meta_file(user_id)
        _meta_information.path = _path_item
        return True

    def list(self, user_id: str) -> ResponseContainer:
        _path_item, _sheet, _wb, _current_file = self.get_sheet(user_id)
        _topic_element = self.get_topic_by_path(_sheet, _path_item)
        return self.get_response_container(_topic_element)

    def delete(self, user_id: str, virtual_index: int) -> bool:
        raise NotImplementedError()

    def current(self, user_id: str) -> str:
        raise NotImplementedError()

    def get_sheet(self, user_id: str) -> \
        (List[PathItem], xmind.core.sheet.SheetElement, xmind.core.workbook.WorkbookDocument, str):
        _, _meta_json = self.read_meta_file(user_id)
        _current_file = _meta_json.current_file
        _current_sheet = _meta_json.current_file.current_sheet
        _xmind_workbook = xmind.load(self.get_full_file_path(user_id, \
                _current_file.file_name))
        _sheet = _xmind_workbook.getSheets()[_current_sheet]
        _path_item: List[PathItem] = self.get_path_item_by_sheet_index(_current_sheet, \
                _meta_json.current_file)
        return _path_item, _sheet, _xmind_workbook, _current_file

    def get_path_item_by_sheet_index(self, sheet_index: int, \
            meta_file_object: MetaFileObject) -> List[PathItem]:
        path: List[PathItem] = []
        for ctx in meta_file_object.context:
            if ctx.sheet_index == sheet_index:
                path.append(ctx)
        
        return sorted(path, key=lambda x: x.step)

    def get_topic_by_path(self, sheet: xmind.core.sheet.SheetElement, path: \
            List[PathItem]) -> TopicElement:
        _root_topic = sheet.getRootTopic()
        if not path:
            return _root_topic
        # navigate to the topic by using part of select function !!!! (without changing the actual path)
        _topic_element = _root_topic
        for _path in path:
            _response_container = self.get_response_container(_topic_element)
            _topic_title = _response_container.get_title_by_index(_path.v_index)
            _topic_elements = _topic_element.getSubTopics()
            _topic_element = self.get_element_by_title(_topic_elements, _topic_title)
        return _topic_element

    def get_element_by_title(self, topics: List[TopicElement], title: str) -> TopicElement:
        for topic in topics:
            if topic.getTitle() == title:
                return topic
        return None
    
    def get_response_container(self, topic_element: TopicElement) -> ResponseContainer:
        _topic_elements = topic_element.getSubTopics()
        if _topic_elements:
            _topics = [topic.getTitle() for topic in _topic_elements]
        else:
            _topics = []
        _response_container = ResponseContainer(_topics)
        return _response_container