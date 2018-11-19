from unittest import TestCase
from src.file.metainformation import MetaFileObject, PathItem, MetaJsonInfo, MetaInformation
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
        _path_item = PathItem(step_index=0, virtual_index=0, sheet_index=0)
        _json_value = _path_item.to_json()
        self.assertIsNotNone(_json_value)

        _file_object = MetaFileObject(file='abc.file', is_locked=False, \
                context=[_path_item], current_sheet=0)
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

    def test_remove_file_from_meta_info(self):
        _user = UserObject(self._user_id)
        _user.working_dir = self._working_dir
        _file_operations = FileOperations(_user)
        _file_operations._create_meta_file(f"{self._user_id}.meta")

        _file_operations.create(self._test_file)
        _file_operations.create(self._test_file + "2")

        _file_operations.delete(self._test_file)
        _file_operations.delete(self._test_file + "2")

        _file_operations.create(self._test_file + "3")
        _file_operations.create(self._test_file + "4")

        _file_operations.delete(self._test_file + "3")
        _file_operations.delete(self._test_file + "4")
    
    def test_is_current_file_occupied(self):
        _user = UserObject(self._user_id)
        _user.working_dir = self._working_dir
        _file_operations = FileOperations(_user)
        _file_operations.create(self._test_file)
        _meta_information = _file_operations.meta_info
        _current_file = _meta_information.current_file.file_name
        self.assertEqual(self._test_file, _current_file)
        self.assertFalse(_meta_information.is_current_file_occupied())
        _meta_information.occupy_current_file()
        self.assertTrue(_meta_information.is_current_file_occupied())
        
        _file_in_general_section = MetaInformation.get_file_object_by_name(_meta_information.meta_file, _current_file)
        self.assertTrue(_file_in_general_section.locked)

    def test_change_path(self):
        _user = UserObject(self._user_id)
        _user.working_dir = self._working_dir
        _file_operations = FileOperations(_user)
        _file_operations.create(self._test_file)
        _meta_information = _file_operations.meta_info
        _list = list(_meta_information.path)
        self.assertTrue(len(_list) == 1)
        _list.append(PathItem(step_index=1, virtual_index=0, sheet_index=0))
        _meta_information.path = _list
        self.assertTrue(len(list(_meta_information.path)) == 2)

