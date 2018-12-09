from unittest import TestCase
from shutil import rmtree as removedirs
from src.controllers.implementations.TopicCommandsProcessor import \
    TopicCommandsProcessor
from src.controllers.implementations.SheetCommandsProcessor import \
    SheetCommandsProcessor
from src.controllers.implementations.FileCommandsProcessor import \
    FileCommandsProcessor


class TopicCommandsProcessorTest(TestCase):
    """Topic commands tests"""

    def setUp(self):
        self._user_id = 'test_user_id'
        self._sheet_cp = SheetCommandsProcessor()
        self._topic_cp = TopicCommandsProcessor()
        self._file_cp = FileCommandsProcessor()
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.select(self._user_id, 0)
        self.assertTrue(_result)

    def tearDown(self):
        # import ipdb
        # ipdb.set_trace()
        removedirs(self._user_id)

    def test_create(self):
        _result = self._topic_cp.create(self._user_id, 'NewTopic1')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, 'NewTopic2')
        self.assertTrue(_result)
        _rc = self._topic_cp.list(self._user_id)
        self.assertListEqual(_rc.titles, ["NewTopic1", "NewTopic2"])

