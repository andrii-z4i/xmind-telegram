from unittest import TestCase
from unittest.mock import patch, Mock

from controllers.implementations.QueueChannel import QueueChannel


class QueueChannelTest(TestCase):

    @patch("controllers.implementations.QueueChannel.ConnectionParameters")
    @patch("controllers.implementations.QueueChannel.BlockingConnection")
    def test_constructor(self, connection: Mock, parameters: Mock):
        _new_channel, _new_connection = self.prepare_channel(connection, parameters)
        _queue_channel = QueueChannel('a', 22, 'qqqq')

        self.assertEqual(_queue_channel._connection, _new_connection)
        self.assertEqual(_queue_channel._channel, _new_channel)
        self.assertEqual(_queue_channel._queue_name, 'qqqq')
        self.assertIsNone(_queue_channel._consumer_tag)
        self.assertIsNone(_queue_channel._callback)
        parameters.assert_called_once_with('a', 22)
        connection.assert_called_once_with('ConnectionParameters')
        _new_connection.channel.assert_called_once()
        del _queue_channel
        _new_connection.close.assert_called_once()

    @patch("controllers.implementations.QueueChannel.ConnectionParameters")
    @patch("controllers.implementations.QueueChannel.BlockingConnection")
    def test_declare_queue(self, connection: Mock, parameters: Mock):
        _new_channel, _new_connection = self.prepare_channel(connection, parameters)
        _new_channel.queue_declare.return_value = None
        _new_channel.basic_qos.return_value = None
        _queue_channel = QueueChannel('a', 22, 'qqqq')
        self.assertIsNotNone(_queue_channel)
        _queue_channel.declare_queue()
        _new_channel.queue_declare.assert_called_once_with(queue='qqqq', durable=True)
        _new_channel.basic_qos.assert_called_once_with(prefetch_count=1)

    @patch("controllers.implementations.QueueChannel.ConnectionParameters")
    @patch("controllers.implementations.QueueChannel.BlockingConnection")
    def test_set_inner_message_processor(self, connection: Mock, parameters: Mock):
        self.prepare_channel(connection, parameters)
        _queue_channel = QueueChannel('a', 22, 'qqqq')
        self.assertIsNotNone(_queue_channel)

        def test_callbck(a: dict) -> None:
            pass

        _queue_channel.set_inner_message_processor(test_callbck)
        self.assertEqual(_queue_channel._callback, test_callbck)

    @patch("controllers.implementations.QueueChannel.ConnectionParameters")
    @patch("controllers.implementations.QueueChannel.BlockingConnection")
    def test_activate_consumer(self, connection: Mock, parameters: Mock):
        _new_channel, _ = self.prepare_channel(connection, parameters)
        _new_channel.basic_consume.return_value = 'new_tag'
        _new_channel.start_consuming.return_value = None
        _queue_channel = QueueChannel('a', 22, 'qqqq')
        self.assertIsNotNone(_queue_channel)
        _queue_channel.activate_consumer()
        _new_channel.basic_consume.assert_called_once_with(_queue_channel._inner_processing, queue='qqqq')
        _new_channel.start_consuming.assert_called_once()
        self.assertEqual(_queue_channel._consumer_tag, 'new_tag')

    @patch("controllers.implementations.QueueChannel.ConnectionParameters")
    @patch("controllers.implementations.QueueChannel.BlockingConnection")
    def test_deactivate_consumer(self, connection: Mock, parameters: Mock):
        _new_channel, _ = self.prepare_channel(connection, parameters)
        _new_channel.stop_consuming.return_value = None
        _queue_channel = QueueChannel('a', 22, 'qqqq')
        self.assertIsNotNone(_queue_channel)
        _queue_channel._consumer_tag = 'new_consumer_tag'
        _queue_channel.deactivate_consumer()
        _new_channel.stop_consuming.assert_called_once_with('new_consumer_tag')

    @patch("controllers.implementations.QueueChannel.ConnectionParameters")
    @patch("controllers.implementations.QueueChannel.BlockingConnection")
    def test__inner_processing(self, connection: Mock, parameters: Mock):
        _new_channel, _ = self.prepare_channel(connection, parameters)
        _new_channel.stop_consuming.return_value = None
        _queue_channel = QueueChannel('a', 22, 'qqqq')
        self.assertIsNotNone(_queue_channel)
        _ch: Mock = Mock()
        _ch.basic_ack.return_value = None
        _method: Mock = Mock(delivery_tag='super_tag')
        _queue_channel.set_inner_message_processor(lambda x: self.assertIsNotNone(x))
        _queue_channel._inner_processing(_ch, _method, None, b'{"test1": 12}')
        _ch.basic_ack.assert_called_once_with(delivery_tag='super_tag')

    @staticmethod
    def prepare_channel(connection: Mock, parameters: Mock) -> (Mock, Mock):
        _new_channel = Mock()
        _new_connection = Mock()
        _new_connection.channel.return_value = _new_channel
        _new_connection.close.return_value = None
        connection.return_value = _new_connection
        parameters.return_value = 'ConnectionParameters'
        return _new_channel, _new_connection
