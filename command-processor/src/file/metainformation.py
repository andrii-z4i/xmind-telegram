"""Mata information processing"""

import json
from typing import List
from src.file.user import UserObject
from src.file.utility import FileUtility
from jsonobject import JsonObject, StringProperty, BooleanProperty, ListProperty, ObjectProperty, IntegerProperty


class PathItem(JsonObject):
    """path item"""
    step = IntegerProperty(name='step_index', required=True)
    v_index = IntegerProperty(name='virtual_index', required=True)


class MetaFileObject(JsonObject):
    """meta file object"""
    file_name = StringProperty(name='file', required=True)
    locked = BooleanProperty(name='is_locked', required=True)
    context = ListProperty(name='context', required=True, item_type=PathItem)


class MetaJsonInfo(JsonObject):
    """meta json information"""
    files = ListProperty(MetaFileObject)
    current_file = ObjectProperty(MetaFileObject)


class DoesNotExistException(Exception):
    """Exception for the case when something doesn't exist"""
    def __init__(self, *args, **kwargs):
        """constructor"""
        super().__init__(args, kwargs)


class MetaInformation(object):

    def __init__(self, user: UserObject):
        if not user:
            raise Exception('User has to be set')

        self._user: UserObject = user
        self._meta_file_path: str = f"{self._user.working_dir}/{self._user.user_id}.meta"
        self._meta_file_name: str = f"{self._user.user_id}.meta"

    def is_current_file_occupied(self) -> bool:
        if not FileUtility.file_exists(self._meta_file_path):
            FileUtility.create_file(self._meta_file_path, None)
            return False

        meta_json_info: MetaJsonInfo = self.read_meta_file()
        return meta_json_info.current_file.locked

    def read_meta_file(self) -> MetaJsonInfo:
        if not FileUtility.file_exists(self._meta_file_path):
            raise DoesNotExistException("Meta file doesn't exist")
        content: dict = FileUtility.read_file_as_dict(self._meta_file_path)
        meta_json_info = MetaJsonInfo(content)
        return meta_json_info

    def _write_meta_file(self, meta_json_info: MetaJsonInfo) -> None:
        if not FileUtility.file_exists(self._meta_file_path):
            FileUtility.create_file(self._meta_file_path, None)

        with open(self._meta_file_path, "w+t") as file_to_write:
            file_to_write.write(json.dumps(meta_json_info.to_json()))

    @property
    def current_file(self) -> MetaFileObject:
        meta_json_info: MetaJsonInfo = self.read_meta_file()
        current_file = meta_json_info.current_file
        return current_file

    @property
    def meta_file_path(self):
        return self._meta_file_path

    @property
    def meta_file_name(self):
        return self._meta_file_name

    def occupy_current_file(self) -> None:
        meta_json_info: MetaJsonInfo = self.read_meta_file()
        _current_file_name = meta_json_info.current_file.file_name
        if meta_json_info.current_file.locked:
            raise Exception('File is occupied')
        meta_json_info.current_file.locked = True
        # search the file in general section and lock it there as well
        _file_in_general_section = \
            MetaInformation.get_file_object_by_name(meta_json_info, _current_file_name)

        if _file_in_general_section:
            _file_in_general_section.locked = True

        self._write_meta_file(meta_json_info)

    @staticmethod
    def enumerate_files(meta_json_info: MetaJsonInfo) -> List[str]:
        for file in meta_json_info.files:
            yield file.file_name

    @staticmethod
    def get_file_object_by_name(meta_json_info: MetaJsonInfo, file_name: str) -> MetaFileObject:
        for _file in meta_json_info.files:
            if _file.file_name == file_name:
                return _file
        return None

    @property
    def path(self) -> List[PathItem]:
        current_file = self.current_file
        for path in current_file.context:
            yield path

    @path.setter
    def path(self, new_path: List[PathItem]) -> None:
        meta_json_info: MetaJsonInfo = self.read_meta_file()
        meta_json_info.current_file.context = new_path
        _file_in_general_section = \
                MetaInformation.get_file_object_by_name(meta_json_info, self.current_file.file_name)

        if _file_in_general_section:
            _file_in_general_section.context = new_path

        self._write_meta_file(meta_json_info)

    @property
    def meta_file(self) -> MetaJsonInfo:
        return self.read_meta_file()

    def add_file(self, new_file_name: str) -> None:
        meta_json_info: MetaJsonInfo = self.read_meta_file()

        if new_file_name in self.enumerate_files(meta_json_info):
            raise Exception('File with a passed name already exists')

        _path_item = PathItem(step_index=0, virtual_index=0)

        _new_file = MetaFileObject(file=new_file_name, is_locked=False, context=[_path_item])
        meta_json_info.files.append(_new_file)
        self._write_meta_file(meta_json_info)

    def change_current_file(self, new_file_name: str) -> None:
        meta_json_info: MetaJsonInfo = self.read_meta_file()

        if new_file_name not in self.enumerate_files(meta_json_info):
            raise Exception('File with passed name doesn\'t exist')

        if self.current_file and new_file_name == self.current_file.file_name:
            return

        for file_object in meta_json_info.files:
            if file_object.file_name != new_file_name:
                continue

            meta_json_info.current_file = file_object

        self._write_meta_file(meta_json_info)

    def remove_file(self, file_name: str) -> None:
        meta_json_info: MetaJsonInfo = self.read_meta_file()

        if len(meta_json_info.files) > 1 and self.current_file.file_name == file_name:
            raise Exception("Current file can't be removed")

        if file_name not in self.enumerate_files(meta_json_info):
            raise Exception("File doesn't exist")

        for file_object in meta_json_info.files:
            if file_object.file_name == file_name:
                meta_json_info.files.remove(file_object)
                break

        if not len(meta_json_info.files):
            meta_json_info.current_file = None

        self._write_meta_file(meta_json_info)
