from unittest import TestCase
from unittest.mock import Mock, MagicMock

from app.controllers.user_controller import UserController
from app.dependencies import dependencies


class UserControllerTests(TestCase):

    def setUp(self):
        self.queue = Mock()
        dependencies.queue = self.queue
        self.message_holder = MagicMock()

    def test_get_user_throws_on_add_to_queue(self):
        self.queue.add.side_effect = Exception('Can\'t add')

        controller = UserController(self.message_holder)
        with self.assertRaises(Exception) as ex:
            result = controller.get()
            self.assertIsNone(result)
            self.assertFalse(True)

        self.assertEqual(repr(ex.exception), repr(Exception('Can\'t add')))
        self.queue.add.assert_called_once_with('someValue')

    def test_get_successfully_add_to_queue(self):
        self.queue.add.return_value = True

        controller = UserController(self.message_holder)

        result = controller.get()
        expectation = ({'status': True}, 200)
        self.assertEqual(result, expectation)
        self.queue.add.assert_called_once_with('someValue')
