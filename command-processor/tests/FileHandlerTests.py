from unittest import TestCase

from src.file.metainformation import MetaFileObject, PathItem, MetaJsonInfo
from src.file.operations.file import FileOperations
from src.file.user import UserObject
from src.file.utility import FileUtility


class FileHandlerTestCase(TestCase):

    def setUp(self):
        self._working_dir = './test'
        self._test_file = 'abc.tuc'
        self._user_id = 'user1'
        self._clean_test_environment()

    def tearDown(self):
        self._clean_test_environment()

    def _clean_test_environment(self):
        _meta_file_path = f"{self._working_dir}/{self._user_id}.meta"
        _test_file_path = f"{self._working_dir}/{self._test_file}"
        FileUtility.remove_file(_meta_file_path)
        FileUtility.remove_file(_test_file_path)
        FileUtility.remove_file(self._working_dir)

    def test_create_file(self):
        _user = UserObject(self._user_id)
        _user.working_dir = self._working_dir
        _file_operations = FileOperations(_user)
        _file_operations.create(self._test_file)

    def test_meta_object(self):
        _path_item = PathItem(step_index=0, virtual_index=0)
        _json_value = _path_item.to_json()
        self.assertIsNotNone(_json_value)

        _file_object = MetaFileObject(file='abc.file', is_locked=False, context=[_path_item])
        _json_value = _file_object.to_json()
        self.assertIsNotNone(_json_value)

        _meta_json_info = MetaJsonInfo(current_file=_file_object, files=[_file_object])
        _json_value = _meta_json_info.to_json()
        self.assertIsNotNone(_json_value)

    def test_create_meta_file(self):
        _user = UserObject(self._user_id)
        _user.working_dir = self._working_dir
        _file_operations = FileOperations(_user)
        _file_operations._create_meta_file(f"{self._user_id}.meta")
