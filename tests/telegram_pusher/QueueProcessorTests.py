from unittest import TestCase
from unittest.mock import Mock, patch, ANY
from cmp_telegram_pusher.src.controllers.implementations.QueueProcessor import QueueProcessor
from cmp_telegram_pusher.src.controllers.interfaces import QueueChannel, MessageSender, MessageRegistrar, QueuePusher
from cmp_telegram_pusher.src.exceptions import RetryException, BadResponseException

_predefined_message = {"message_type": "error", "message": {"chat_id": 12, "text": "Hello"}}

class QueueProcessorTests(TestCase):
    def setUp(self):
        self._queue_channel = Mock(spec=QueueChannel)
        self._message_sender = Mock(spec=MessageSender)
        self._message_registrar = Mock(spec=MessageRegistrar)
        self._queue_pusher = Mock(spec=QueuePusher)

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_constructor(self, thread: Mock) -> None:
        thread.return_value = 'super'
        self._queue_channel.set_inner_message_processor.return_value = None
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)
        self.assertEqual(_queue_processor._thread, 'super')
        self._queue_channel.set_inner_message_processor.assert_called_once_with(_queue_processor.process_event)

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_start(self, thread: Mock) -> None:
        _new_thread: Mock = Mock()
        _new_thread.start.return_value = None
        self._queue_channel.activate_consumer.return_value = None

        thread.return_value = _new_thread
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)

        self.assertIsNotNone(_queue_processor)
        _queue_processor.start()
        self._queue_channel.activate_consumer.assert_called_once()
        _new_thread.start.assert_called_once()

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_stop(self, thread: Mock) -> None:
        _new_thread: Mock = Mock()
        _new_thread.join.return_value = None
        self._queue_channel.deactivate_consumer.return_value = None

        thread.return_value = _new_thread
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)

        self.assertIsNotNone(_queue_processor)
        _queue_processor.stop()
        self._queue_channel.deactivate_consumer.assert_called_once()
        _new_thread.join.assert_called_once()

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_process_event_success(self, thread: Mock) -> None:
        thread.return_value = 'super'
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)
        self.assertIsNotNone(_queue_processor)
        self._message_sender.send_message.return_value = None
        self._queue_pusher.put_message_to_queue.return_value = None
        self._message_registrar.store_message.return_value = None

        _queue_processor.process_event(_predefined_message)

        self._message_sender.send_message.assert_called_once()
        self.assertEqual("Hello", self._message_sender.send_message.call_args[0][0].text)
        self.assertEqual(12, self._message_sender.send_message.call_args[0][0].chat_id)
        self._queue_pusher.put_message_to_queue.assert_not_called()
        self._message_registrar.store_message.assert_not_called()

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_process_event_retry_exception(self, thread: Mock) -> None:
        thread.return_value = 'super'
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)
        self.assertIsNotNone(_queue_processor)
        self._message_sender.send_message.side_effect = RetryException(100)
        self._queue_pusher.put_message_to_queue.return_value = True
        self._message_registrar.store_message.return_value = None

        _queue_processor.process_event(_predefined_message)

        self._message_sender.send_message.assert_called_once()
        self.assertEqual("Hello", self._message_sender.send_message.call_args[0][0].text)
        self.assertEqual(12, self._message_sender.send_message.call_args[0][0].chat_id)
        self._queue_pusher.put_message_to_queue.assert_called_once_with(ANY, 100)
        self._message_registrar.store_message.assert_not_called()

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_process_event_retry_exception_fail_to_put_message_to_queue(self, thread: Mock) -> None:
        thread.return_value = 'super'
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)
        self.assertIsNotNone(_queue_processor)
        self._message_sender.send_message.side_effect = RetryException(100)
        self._queue_pusher.put_message_to_queue.return_value = False
        self._message_registrar.store_message.return_value = None

        _queue_processor.process_event(_predefined_message)

        self._message_sender.send_message.assert_called_once()
        self.assertEqual("Hello", self._message_sender.send_message.call_args[0][0].text)
        self.assertEqual(12, self._message_sender.send_message.call_args[0][0].chat_id)
        self._queue_pusher.put_message_to_queue.assert_called_once_with(ANY, 100)
        self._message_registrar.store_message.assert_called_once_with(ANY)

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_process_event_bad_response_exception(self, thread: Mock) -> None:
        thread.return_value = 'super'
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)
        self.assertIsNotNone(_queue_processor)
        self._message_sender.send_message.side_effect = BadResponseException('strange')
        self._queue_pusher.put_message_to_queue.return_value = None
        self._message_registrar.store_message.return_value = None

        _queue_processor.process_event(_predefined_message)

        self._message_sender.send_message.assert_called_once()
        self.assertEqual("Hello", self._message_sender.send_message.call_args[0][0].text)
        self.assertEqual(12, self._message_sender.send_message.call_args[0][0].chat_id)
        self._queue_pusher.put_message_to_queue.assert_not_called()
        self._message_registrar.store_message.assert_called_once_with(ANY)

    @patch("cmp_telegram_pusher.src.controllers.implementations.QueueProcessor.Thread")
    def test_process_event_bad_message_exception(self, thread: Mock) -> None:
        thread.return_value = 'super'
        _queue_processor = QueueProcessor(
            self._queue_channel,
            self._message_sender,
            self._message_registrar,
            self._queue_pusher)
        self.assertIsNotNone(_queue_processor)
        self._message_sender.send_message.side_effect = BadResponseException('strange')
        self._queue_pusher.put_message_to_queue.return_value = None
        self._message_registrar.store_message.return_value = None

        _queue_processor.process_event({})

        self._message_sender.send_message.assert_not_called()
        self._queue_pusher.put_message_to_queue.assert_not_called()
        self._message_registrar.store_message.assert_called_once_with('\\{\\}')