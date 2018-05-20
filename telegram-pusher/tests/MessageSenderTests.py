from unittest import TestCase
from src.controllers.implementations.MessageSender import MessageSender
from src.exceptions import BadResponseException
from src.exceptions.retry_exception import RetryException
from src.model import Message, SentMessage
import json
from unittest.mock import Mock, patch


class MessageSenderTest(TestCase):

    @patch('src.controllers.implementations.MessageSender.post')
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

        ctrl: MessageSender = MessageSender(
            'http', 'localhost', 8080, 'botId:botKey')
        message: Message = Message(chat_id=129868778, text='Super puper')

        server_response = Mock(
            ok=True, content=json.dumps(raw_response).encode())
        requests_post.return_value = server_response
        response: SentMessage = ctrl.send_message(message)

        requests_post.assert_called_once_with(
            'http://localhost:8080/botbotId:botKey/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})

        self.assertEqual(response.chat.chat_id, 129868778)

    @patch('src.controllers.implementations.MessageSender.post')
    def test_send_message_failure(self, requests_post: Mock) -> None:

        ctrl: MessageSender = MessageSender(
            'http', 'localhost', 8080, 'something')
        message: Message = Message(
            chat_id=129868778, text='Super puper')

        server_response = Mock(ok=False, content=json.dumps({}).encode())
        requests_post.return_value = server_response

        with self.assertRaises(BadResponseException) as thrown_exception:
            response = ctrl.send_message(message)

        requests_post.assert_called_once_with(
            'http://localhost:8080/botsomething/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})
        self.assertEqual(
            thrown_exception.exception.reason, "Bad response")

    @patch('src.controllers.implementations.MessageSender.post')
    def test_send_message_returns_error_with_retry(self, requests_post: Mock) -> None:
        raw_response: dict = {
            'ok': False,
            'description': 'We can\'t accept message',
            'parameters': {
                'migrate_to_chat_id': 1122222,
                'retry_after': 11221
            }
        }
        ctrl: MessageSender = MessageSender(
            'http', 'localhost', 8080, 'something')
        message: Message = Message(
            chat_id=129868778, text='Super puper')

        server_response = Mock(
            ok=True, content=json.dumps(raw_response).encode())
        requests_post.return_value = server_response
        with self.assertRaises(RetryException) as _exception:
            response = ctrl.send_message(message)

        self.assertEqual(
            _exception.exception.retry_after, 11221)

        requests_post.assert_called_once_with(
            'http://localhost:8080/botsomething/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})

    @patch('src.controllers.implementations.MessageSender.post')
    def test_send_message_returns_error_without_retry(self, requests_post: Mock) -> None:
        raw_response: dict = {
            'ok': False,
            'description': 'We can\'t accept message'
        }
        ctrl: MessageSender = MessageSender(
            'http', 'localhost', 8080, 'something')
        message: Message = Message(
            chat_id=129868778, text='Super puper')

        server_response = Mock(
            ok=True, content=json.dumps(raw_response).encode())
        requests_post.return_value = server_response

        with self.assertRaises(BadResponseException) as thrown_exception:
            ctrl.send_message(message)

        self.assertEqual(
            thrown_exception.exception.reason, "We got a bad response")
        requests_post.assert_called_once_with(
            'http://localhost:8080/botsomething/sendMessage', json={"chat_id": 129868778, "text": "Super puper"})
