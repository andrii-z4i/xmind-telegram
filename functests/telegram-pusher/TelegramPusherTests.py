from time import sleep
from unittest import TestCase, skip
import mockserver as mk

from common.message_registrar import MessageRegistrar
from common.queue_pusher import QueuePusher
import json


class TelegramPusherTests(TestCase):
    def setUp(self):
        self._mock_server: mk.MockServerClient = mk.MockServerClient(
            "http://localhost:1080")
        self._mock_server.reset()
        self._db: MessageRegistrar = MessageRegistrar(
            "localhost", "badmessages", "test", "test")
        self._db.remove_all_messages()
        self._queue: QueuePusher = QueuePusher('localhost', 5672, 'super')

    @skip('Not needed for now')
    def test_no_ok_in_response(self):
        response = {"error": True}
        self._mock_server.expect(
            mk.request(method="POST", path="/botadfaadf/sendMessage",
                       body=json.dumps({"chat_id": None, "text": None})),
            mk.json_response(200, response),
            mk.times(1))
        self._queue.put_message_to_queue({"something": "do"})
        sleep(1)
        self._mock_server.verify()
        messages = self._db.get_all_message()
        self.assertEqual(1, len(messages))

    def test_404(self):
        response = {"ok": True}
        self._mock_server.expect(
            mk.request(method="POST", path="/botadfaadf/sendMessage",
                       body=json.dumps({"chat_id": None, "text": None})),
            mk.json_response(404, response),
            mk.times(1))
        self._queue.put_message_to_queue({"something": "do"})
        sleep(1)
        self._mock_server.verify()
        messages = self._db.get_all_message()
        self.assertEqual(1, len(messages))
