from src.controllers.interfaces.ResponseContainer import ResponseContainer
from unittest import TestCase


class ResponseContainerTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_indices_generation(self):
        _titles = [
            '_someTitle',
            '__someTitle',
            'aGoodTitle',
            'aBadTitle',
            'superTitle',
            'superTitle2',
            '12',
            '0'
        ]
        _response_container = ResponseContainer(_titles)
        self.assertEqual(8, len(_response_container.titles))
        self.assertEqual(8, len(_response_container.indices))
        self.assertEqual(7, _response_container.indices[7])
        self.assertEqual('0', _response_container.titles[0])
        self.assertEqual('__someTitle', _response_container.get_title_by_index(2))
        self.assertEqual('superTitle2', _response_container.get_title_by_index(7))
