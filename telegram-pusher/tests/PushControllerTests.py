from unittest import TestCase
from controller.PushController import PushController
from model import Message, SentMessage
import json
from unittest.mock import Mock, patch


class PushControllerTest(TestCase):
    def setUp(self):
        self._queue_pusher = Mock()
        self._queue_pusher.put_message_to_queue.return_value = True

    @patch('controller.PushController.post')
    def test_send_message_success(self, requests_post: Mock) -> None:
        raw_response: dict = {
            'ok': True,
            'result': {
                'message_id': 32,
                'from': {
                    'id': 548593134,
                    'is_bot': True,
                    'first_name': 'xmindbot',
                    'username': 'xminderbot'
                },
                'chat': {
                    'id': 129868778,
                    'first_name': 'Andrii',
                    'last_name': 'z4i',
                    'username': 'Andrii_z4i',
                    'type': 'private'},
                'date': 1523186184,
                'text': 'Super puper'
            },
            'description': 'optional field if error occurred',
            'parameters': {
                'migrate_to_chat_id': 1122222,
                'retry_after': 11221
            }
        }

        ctrl: PushController = PushController(
            'http', 'localhost', 8080, 'botId:botKey', self._queue_pusher)
        message: Message = Message(chat_id=129868778, text='Super puper')

        server_response = Mock(
            ok=True, content=json.dumps(raw_response).encode())
        requests_post.return_value = server_response
        response: SentMessage = ctrl.send_message(message)

        requests_post.assert_called_once_with(
            'http://localhost:8080/botbotId:botKey/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})

        self.assertEqual(response.chat.chat_id, 129868778)
        self._queue_pusher.put_message_to_queue.assert_not_called()

    @patch('controller.PushController.post')
    def test_send_message_failure(self, requests_post: Mock) -> None:

        ctrl: PushController = PushController(
            'http', 'localhost', 8080, 'something', self._queue_pusher)
        message: Message = Message(
            chat_id=129868778, text='Super puper')

        server_response = Mock(ok=False, content=json.dumps({}).encode())
        requests_post.return_value = server_response

        with self.assertRaises(Exception) as thrown_exception:
            response = ctrl.send_message(message)

        requests_post.assert_called_once_with(
            'http://localhost:8080/botsomething/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})
        self.assertEqual(
            thrown_exception.exception.args[0], "Bad response")
        self._queue_pusher.put_message_to_queue.assert_not_called()

    @patch('controller.PushController.post')
    def test_send_message_returns_error_with_retry(self, requests_post: Mock) -> None:
        raw_response: dict = {
            'ok': False,
            'description': 'We can\'t accept message',
            'parameters': {
                'migrate_to_chat_id': 1122222,
                'retry_after': 11221
            }
        }
        ctrl: PushController = PushController(
            'http', 'localhost', 8080, 'something', self._queue_pusher)
        message: Message = Message(
            chat_id=129868778, text='Super puper')

        server_response = Mock(
            ok=True, content=json.dumps(raw_response).encode())
        requests_post.return_value = server_response
        response = ctrl.send_message(message)
        self.assertIsNone(response)
        requests_post.assert_called_once_with(
            'http://localhost:8080/botsomething/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})
        self._queue_pusher.put_message_to_queue.assert_called_once_with(message, 11221)

    @patch('controller.PushController.post')
    def test_send_message_returns_error_without_retry(self, requests_post: Mock) -> None:
        raw_response: dict = {
            'ok': False,
            'description': 'We can\'t accept message'
        }
        ctrl: PushController = PushController(
            'http', 'localhost', 8080, 'something', self._queue_pusher)
        message: Message = Message(
            chat_id=129868778, text='Super puper')

        server_response = Mock(
            ok=True, content=json.dumps(raw_response).encode())
        requests_post.return_value = server_response

        with self.assertRaises(Exception) as thrown_exception:
            response = ctrl.send_message(message)

        self.assertEqual(
            thrown_exception.exception.args[0], "We got a bad response")
        requests_post.assert_called_once_with(
            'http://localhost:8080/botsomething/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})
        self._queue_pusher.put_message_to_queue.assert_not_called()

