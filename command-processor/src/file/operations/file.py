import os

from src.file.user import UserObject
import src.file.metainformation as metainfo
import src.file.utility as utility
import json


class FileOperations(object):

    def __init__(self, user: UserObject):
        if not user:
            raise Exception('User object is empty')

        self._user = user
        self._meta_info = metainfo.MetaInformation(self._user)

    def create(self, file_name: str) -> None:

        try:
            meta_file = self._meta_info.meta_file
        except metainfo.DoesNotExistException:
            self._create_meta_file(file_name)
            return

        if file_name in self._meta_info.enumerate_files(meta_file):
            raise Exception('File already exists')
        if utility.FileUtility.file_exists(file_name):
            raise Exception('File already exists, but is not present in meta info')

        utility.FileUtility.create_file(file_name, None)
        self._meta_info.change_current_file(file_name)

    def _create_meta_file(self, file_name: str) -> None:
        utility.FileUtility.create_folder(self._user.working_dir)

        _path_item = metainfo.PathItem(step_index=0, virtual_index=0)
        _file_object = metainfo.MetaFileObject(file=file_name, is_locked=False, context=[_path_item])
        _meta_json_info = metainfo.MetaJsonInfo(current_file=_file_object, files=[_file_object])
        _json_value = _meta_json_info.to_json()
        _file_full_path = f"{self._user.working_dir}/{file_name}"
        utility.FileUtility.create_file(_file_full_path, None)
        utility.FileUtility.create_file(self._meta_info.meta_file_path, json.dumps(_json_value))

    def delete(self, file_name: str) -> None:
        meta_file = self._meta_info.meta_file
        if file_name not in self._meta_info.enumerate_files(meta_file):
            raise Exception("File doesn't exist")


