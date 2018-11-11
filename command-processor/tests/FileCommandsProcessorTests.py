from unittest import TestCase
from shutil import rmtree as removedirs
from src.controllers.implementations.FileCommandsProcessor import \
FileCommandsProcessor


class FileCommandsProcessorTest(TestCase):
    def setUp(self):
        self._user_id = 'test_user_id'
        self._file_cp = FileCommandsProcessor()

    def tearDown(self):
        removedirs(self._user_id)

    def test_create(self):
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)

    def test_list(self):
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.create(self._user_id, 'some_file1.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.create(self._user_id, 'some_file2.xmind')
        self.assertTrue(_result)

        _list = self._file_cp.list(self._user_id)
        self.assertEqual(3, len(_list.indices))
        self.assertEqual(3, len(_list.titles))
        self.assertListEqual(['some_file.xmind', 'some_file1.xmind', \
            'some_file2.xmind'], _list.titles)

    def test_delete(self):
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.create(self._user_id, 'some_file1.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.create(self._user_id, 'some_file2.xmind')
        self.assertTrue(_result)

        _list = self._file_cp.list(self._user_id)
        self.assertEqual(3, len(_list.indices))
        self.assertEqual(3, len(_list.titles))
        self.assertListEqual(['some_file.xmind', 'some_file1.xmind', \
            'some_file2.xmind'], _list.titles)
        _result = self._file_cp.delete(self._user_id, 1)
        self.assertTrue(_result)
        _list2 = self._file_cp.list(self._user_id)
        self.assertEqual(2, len(_list2.indices))
        self.assertEqual(2, len(_list2.titles))
        self.assertListEqual(['some_file.xmind', \
            'some_file2.xmind'], _list2.titles)

    def test_select(self):
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.create(self._user_id, 'some_file1.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.create(self._user_id, 'some_file2.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.select(self._user_id, 1)
        self.assertTrue(_result)
        _current_file = self._file_cp.current(self._user_id)
        self.assertEqual(_current_file, "some_file1.xmind")
        _result = self._file_cp.select(self._user_id, -1)
        self.assertFalse(_result)
