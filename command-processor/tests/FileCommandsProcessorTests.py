from unittest import TestCase
from src.controllers.implementations.FileCommandsProcessor import \
FileCommandsProcessor


class FileCommandsProcessorTest(TestCase):
    def setUp(self):
        self._user_id = 'test_user_id'
        self._file_cp = FileCommandsProcessor()

    def tearDown(self):
        pass

    def test_create(self):
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)
