import os
import json
from src.file.user import UserObject
import src.file.metainformation as metainfo
from src.file import utility


class FileOperations(object):

    def __init__(self, user: UserObject):
        if not user:
            raise Exception('User object is empty')

        self._user = user
        self._meta_info = metainfo.MetaInformation(self._user)

    @property
    def meta_info(self):
        return self._meta_info

    def create(self, file_name: str) -> None:

        try:
            meta_file = self._meta_info.meta_file
        except metainfo.DoesNotExistException:
            self._create_meta_file(self._meta_info.meta_file_name)
            meta_file = self._meta_info.meta_file

        if file_name in self._meta_info.enumerate_files(meta_file):
            raise Exception('File already exists')
        if utility.FileUtility.file_exists(file_name):
            raise Exception('File already exists, but is not present in meta info')

        _file_full_path = f"{self._user.working_dir}/{file_name}"
        utility.FileUtility.create_file(_file_full_path, None)
        self._meta_info.add_file(file_name)
        self._meta_info.change_current_file(file_name)

    def _create_meta_file(self, file_name: str) -> None:
        utility.FileUtility.create_folder(self._user.working_dir)
        _meta_json_info = metainfo.MetaJsonInfo(current_file=None, files=[])
        _json_value = _meta_json_info.to_json()
        _file_full_path = f"{self._user.working_dir}/{file_name}"
        utility.FileUtility.create_file(_file_full_path, None)
        utility.FileUtility.create_file(self._meta_info.meta_file_path, json.dumps(_json_value))

    def delete(self, file_name: str) -> None:
        meta_file = self._meta_info.meta_file
        if file_name not in self._meta_info.enumerate_files(meta_file):
            raise Exception("File doesn't exist")

        self._meta_info.remove_file(file_name)
        _file_full_path = f"{self._user.working_dir}/{file_name}"
        utility.FileUtility.remove_file(_file_full_path)


