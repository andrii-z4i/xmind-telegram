from unittest import TestCase
from shutil import rmtree as removedirs
from src.controllers.implementations.SheetCommandsProcessor import SheetCommandsProcessor
from src.controllers.implementations.FileCommandsProcessor import \
FileCommandsProcessor


class SheetCommandsProcessorTest(TestCase):
    """Sheet commands tests"""

    def setUp(self):
        self._user_id = 'test_user_id'
        self._sheet_cp = SheetCommandsProcessor()
        self._file_cp = FileCommandsProcessor()
        _result = self._file_cp.create(self._user_id, 'some_file.xmind')
        self.assertTrue(_result)
        _result = self._file_cp.select(self._user_id, 0)
        self.assertTrue(_result)

    def tearDown(self):
        removedirs(self._user_id)

    def test_create(self):
        _result = self._sheet_cp.create(self._user_id, 'NewSheet')
        self.assertTrue(_result)
        _result = self._sheet_cp.create(self._user_id, 'NewSheet1')
        self.assertTrue(_result)
        _result = self._sheet_cp.create(self._user_id, 'NewSheet2')
        self.assertTrue(_result)
        _sheets = self._sheet_cp.list(self._user_id)
        self.assertEqual(4, len(_sheets.titles))
        self.assertListEqual(['NewSheet', 'NewSheet', 'NewSheet1', \
            'NewSheet2'], _sheets.titles)

    def test_select(self):
        _result = self._sheet_cp.create(self._user_id, 'NewSheet')
        self.assertTrue(_result)
        _result = self._sheet_cp.create(self._user_id, 'NewSheet1')
        self.assertTrue(_result)
        _result = self._sheet_cp.create(self._user_id, 'NewSheet2')
        self.assertTrue(_result)
        _result = self._sheet_cp.select(self._user_id, 3)
        self.assertTrue(_result)
        _current = self._sheet_cp.current(self._user_id)
        self.assertEqual('NewSheet2', _current)

    def test_delete(self):
        _result = self._sheet_cp.create(self._user_id, 'NewSheet0')
        self.assertTrue(_result)
        _result = self._sheet_cp.create(self._user_id, 'NewSheet1')
        self.assertTrue(_result)
        _result = self._sheet_cp.create(self._user_id, 'NewSheet2')
        self.assertTrue(_result)
        _result = self._sheet_cp.delete(self._user_id, 0)
        self.assertTrue(_result)
        _sheets = self._sheet_cp.list(self._user_id)
        self.assertEqual(3, len(_sheets.titles))
        self.assertListEqual(['NewSheet0', 'NewSheet1', \
            'NewSheet2'], _sheets.titles)
        _current = self._sheet_cp.current(self._user_id)
        self.assertEqual('NewSheet0', _current)
