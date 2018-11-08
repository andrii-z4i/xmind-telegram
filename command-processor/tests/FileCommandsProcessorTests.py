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
