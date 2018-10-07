from typing import List
from src.file.user import UserObject
from src.file.utility import FileUtility
from jsonobject import JsonObject, StringProperty, BooleanProperty, ListProperty, ObjectProperty, IntegerProperty
import json


class PathItem(JsonObject):
    step = IntegerProperty(name='step_index', required=True)
    v_index = IntegerProperty(name='virtual_index', required=True)


class MetaFileObject(JsonObject):
    file_name = StringProperty(name='file', required=True)
    locked = BooleanProperty(name='is_locked', required=True)
    context = ListProperty(name='context', required=True, item_type=PathItem)


class MetaJsonInfo(JsonObject):
    files = ListProperty(MetaFileObject)
    current_file = ObjectProperty(MetaFileObject)


class DoesNotExistException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class MetaInformation(object):

    def __init__(self, user: UserObject):
        if not user:
            raise Exception('User has to be set')

        self._user: UserObject = user
        self._meta_file_path: str = f"{self._user.working_dir}/{self._user.user_id}.meta"

    def is_current_file_occupied(self) -> bool:
        if not FileUtility.file_exists(self._meta_file_path):
            FileUtility.create_file(self._meta_file_path, None)
            return False

        meta_json_info: MetaJsonInfo = self._read_meta_file()
        return meta_json_info.current_file.locked

    def _read_meta_file(self) -> MetaJsonInfo:
        if not FileUtility.file_exists(self._meta_file_path):
            raise DoesNotExistException("Meta file doesn't exist")
        content: dict = FileUtility.read_file_as_dict(self._meta_file_path)
        meta_json_info = MetaJsonInfo(content)
        return meta_json_info

    def _write_meta_file(self, meta_json_info: MetaJsonInfo) -> None:
        if not FileUtility.file_exists(self._meta_file_path):
            FileUtility.create_file(self._meta_file_path, None)

        with open(self._meta_file_path, "w+t") as f:
            f.write(json.dumps(meta_json_info.to_json()))

    @property
    def _current_file(self) -> MetaFileObject:
        meta_json_info: MetaJsonInfo = self._read_meta_file()
        current_file = meta_json_info.current_file
        return current_file

    @property
    def meta_file_path(self):
        return self._meta_file_path

    def occupy_current_file(self) -> None:
        meta_json_info: MetaJsonInfo = self._read_meta_file()
        if meta_json_info.current_file.locked:
            raise Exception('File is occupied')
        meta_json_info.current_file.locked = True
        self._write_meta_file(meta_json_info)

    @staticmethod
    def enumerate_files(meta_json_info: MetaJsonInfo) -> List[str]:
        for file in meta_json_info.files:
            yield file.file_name

    @property
    def path(self) -> List[PathItem]:
        current_file = self._current_file
        for path in current_file.context:
            yield path

    @path.setter
    def path(self, new_path: List[PathItem]) -> None:
        meta_json_info: MetaJsonInfo = self._read_meta_file()
        meta_json_info.current_file.context = ListProperty(new_path)
        self._write_meta_file(meta_json_info)

    @property
    def meta_file(self) -> MetaJsonInfo:
        return self._read_meta_file()

    def add_file(self, new_file_name: str) -> None:
        meta_json_info: MetaJsonInfo = self._read_meta_file()

        if new_file_name in self.enumerate_files(meta_json_info):
            raise Exception('File with a passed name already exists')

        _new_file = MetaFileObject(file=new_file_name, is_locked=False, context=[])
        meta_json_info.files.append(_new_file)

    def change_current_file(self, new_file_name: str) -> None:
        meta_json_info: MetaJsonInfo = self._read_meta_file()

        if new_file_name not in self.enumerate_files(meta_json_info):
            raise Exception('No file with passed name exists')

        if new_file_name == self._current_file.file_name:
            return  # noop needed

        for file_object in meta_json_info.files:
            if file_object.file_name != new_file_name:
                continue

            meta_json_info.current_file = file_object

        self._write_meta_file(meta_json_info)

    def remove_file(self, file_name: str) -> None:
        if self._current_file.file_name == file_name:
            raise Exception("Current file can't be removed")

        meta_json_info: MetaJsonInfo = self._read_meta_file()

        if file_name not in self.enumerate_files(meta_json_info):
            raise Exception("File doesn't exist")

        for file_object in meta_json_info.files:
            if file_object.file_name == file_name:
                meta_json_info.files.remove(file_object)
                break


