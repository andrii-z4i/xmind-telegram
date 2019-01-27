from unittest import TestCase
from unittest.mock import Mock, patch
from cmp_telegram_pusher.src.controllers.implementations.QueuePusher import QueuePusher
from shared.model import MessageContainer

_predefined_message = {"message_type": "error",
                       "message": {"chat_id": 12, "text": "Hello"}}


class QueuePusherTests(TestCase):
    def setUp(self):
        pass

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.ConnectionParameters")
    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.BlockingConnection")
    def test_constructor(self, connection: Mock, connection_parameters: Mock) -> None:
        _new_blocking_connection: Mock = Mock()
        _new_blocking_connection.channel.return_value = 'channel'
        _new_blocking_connection.close.return_value = None

        connection_parameters.return_value = 'new_parameters'
        connection.return_value = _new_blocking_connection
        _queue_pusher = QueuePusher('server', 1111, 'qqqq')
        self.assertIsNotNone(_queue_pusher)
        self.assertEqual(_queue_pusher._connection, _new_blocking_connection)
        self.assertEqual(_queue_pusher._queue_name, 'qqqq')
        self.assertEqual(_queue_pusher._channel, 'channel')
        connection.assert_called_once_with('new_parameters')
        connection_parameters.assert_called_once_with(
            'server', 1111, connection_attempts=3, retry_delay=5)
        _new_blocking_connection.channel.assert_called_once()

        del _queue_pusher
        _new_blocking_connection.close.assert_called_once()

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.ConnectionParameters")
    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.BlockingConnection")
    def test_put_message_to_queue_exception(self, connection: Mock, connection_parameters: Mock) -> None:
        _new_blocking_connection: Mock = Mock()
        _new_blocking_connection.channel.return_value = None

        connection_parameters.return_value = 'new_parameters'
        connection.return_value = _new_blocking_connection
        _queue_pusher = QueuePusher('server', 1111, 'qqqq')
        self.assertIsNotNone(_queue_pusher)

        _message_container: MessageContainer = MessageContainer(
            _predefined_message)

        with self.assertRaises(Exception) as _exception:
            _queue_pusher.put_message_to_queue(_message_container, 500)

        self.assertEqual(_exception.exception.args[0], "Channel is not set")

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.BasicProperties")
    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.ConnectionParameters")
    @patch("cmp_telegram_pusher.src.controllers.implementations.QueuePusher.pika.BlockingConnection")
    def test_put_message_to_queue_success(
            self,
            connection: Mock,
            connection_parameters: Mock,
            basic_properties: Mock
    ) -> None:
        _channel: Mock = Mock()
        _channel.basic_publish.return_value = True

        _new_blocking_connection: Mock = Mock()
        _new_blocking_connection.channel.return_value = _channel

        connection_parameters.return_value = 'new_parameters'
        connection.return_value = _new_blocking_connection

        basic_properties.return_value = 'basic_properties'

        _queue_pusher = QueuePusher('server', 1111, 'qqqq')
        self.assertIsNotNone(_queue_pusher)

        _message_container: MessageContainer = MessageContainer(
            _predefined_message)
        self.assertTrue(_queue_pusher.put_message_to_queue(
            _message_container, 500))
        _expected_body = '{"message_type": "error", "message": {"chat_id": 12, "text": "Hello"}, "retry_count": 1, ' \
                         '"retry_after": 500}'
        _channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='qqqq',
            body=_expected_body,
            properties='basic_properties')
        basic_properties.assert_called_once_with(delivery_mode=2)
