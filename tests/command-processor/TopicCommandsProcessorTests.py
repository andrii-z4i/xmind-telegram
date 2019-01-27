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

    def test_select(self):
        _result = self._topic_cp.create(self._user_id, 'NewTopic1')
        self.assertTrue(_result)
        _result = self._topic_cp.select(self._user_id, 0)
        _result = self._topic_cp.create(self._user_id, 'NewTopic2')
        self.assertTrue(_result)
        _rc = self._topic_cp.list(self._user_id)
        self.assertTrue(len(_rc.titles) == 1)
        _result = self._topic_cp.select(self._user_id, 0)
        _rc = self._topic_cp.list(self._user_id)
        self.assertTrue(len(_rc.titles) == 0)
        
    def test_select_up(self):
        _result = self._topic_cp.create(self._user_id, 'NewTopic1')
        self.assertTrue(_result)
        _result = self._topic_cp.select(self._user_id, 0)
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, 'NewTopic2')
        self.assertTrue(_result)
        _result = self._topic_cp.select(self._user_id, 0)
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, 'NewTopic3')
        self.assertTrue(_result)
        _result = self._topic_cp.select(self._user_id, 0)
        self.assertTrue(_result)
        _rc = self._topic_cp.list(self._user_id)
        # last item, no subtopics
        self.assertTrue(len(_rc.titles) == 0)
        _result = self._topic_cp.select(self._user_id, -1)
        self.assertTrue(_result)
        _rc = self._topic_cp.list(self._user_id)
        self.assertTrue(len(_rc.titles) == 1)
        self.assertEqual(_rc.titles[0], "NewTopic3")
        _result = self._topic_cp.select(self._user_id, -1)
        self.assertTrue(_result)
        _rc = self._topic_cp.list(self._user_id)
        self.assertTrue(len(_rc.titles) == 1)
        self.assertEqual(_rc.titles[0], "NewTopic2")
        _result = self._topic_cp.select(self._user_id, 0)
        _rc = self._topic_cp.list(self._user_id)
        self.assertTrue(len(_rc.titles) == 1)

    def test_current(self):
        _result = self._topic_cp.create(self._user_id, '1')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '2')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3')
        self.assertTrue(_result)
        _rc = self._topic_cp.current(self._user_id)
        self.assertEqual(1, len(_rc.titles))
        self.assertEqual('NewTopic', _rc.titles[0])
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(3, len(_rc.titles))
        self.assertListEqual(['1', '2', '3'], _rc.titles)
        _result = self._topic_cp.select(self._user_id, 2)
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3.1')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3.2')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3.3')
        self.assertTrue(_result)
        _rc = self._topic_cp.current(self._user_id)
        self.assertEqual(1, len(_rc.titles))
        self.assertEqual('3', _rc.titles[0])
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(3, len(_rc.titles))
        self.assertListEqual(['3.1', '3.2', '3.3'], _rc.titles)

    def test_delete(self):
        _result = self._topic_cp.create(self._user_id, '1')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '2')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3')
        self.assertTrue(_result)
        _rc = self._topic_cp.current(self._user_id)
        self.assertEqual(1, len(_rc.titles))
        self.assertEqual('NewTopic', _rc.titles[0])
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(3, len(_rc.titles))
        self.assertListEqual(['1', '2', '3'], _rc.titles)
        _result = self._topic_cp.select(self._user_id, 2)
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3.1')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3.2')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '3.3')
        self.assertTrue(_result)

        _result = self._topic_cp.select(self._user_id, -1)
        self.assertTrue(_result)
        _result = self._topic_cp.select(self._user_id, 1)
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '2.1')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '2.2')
        self.assertTrue(_result)
        _result = self._topic_cp.create(self._user_id, '2.3')
        self.assertTrue(_result)

        _result = self._topic_cp.select(self._user_id, -1)
        self.assertTrue(_result)
        _result = self._topic_cp.select(self._user_id, 2)
        self.assertTrue(_result)

        _rc = self._topic_cp.current(self._user_id)
        self.assertEqual(1, len(_rc.titles))
        self.assertEqual('3', _rc.titles[0])
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(3, len(_rc.titles))
        self.assertListEqual(['3.1', '3.2', '3.3'], _rc.titles)
        self.assertTrue(self._topic_cp.delete(self._user_id, 0))
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(2, len(_rc.titles))
        self.assertListEqual(['3.2', '3.3'], _rc.titles)
        self.assertTrue(self._topic_cp.select(self._user_id, -1))  # up
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(3, len(_rc.titles))
        self.assertListEqual(['1', '2', '3'], _rc.titles)
        self.assertTrue(self._topic_cp.delete(self._user_id, 1))
        _rc = self._topic_cp.list(self._user_id)
        self.assertEqual(2, len(_rc.titles))
        self.assertListEqual(['1', '3'], _rc.titles)

        
        