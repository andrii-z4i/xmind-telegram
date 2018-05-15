import json
import pika
import src.controllers.interfaces as interfaces
from src.model import MessageContainer


class QueuePusher(interfaces.QueuePusher):

    def __init__(self, queue_server: str, queue_port: int, queue_name: str):
        super().__init__()
        self._queue_name = queue_name
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(queue_server, queue_port))
        self._channel = self._connection.channel()

    def __del__(self):
        _connection = getattr(self, "_connection", None)
        if _connection and _connection.is_open:
            _connection.close()

    def put_message_to_queue(self, message: MessageContainer, retry_after: int) -> bool:
        if self._channel:
            message.retry_count = 1 if not message.retry_count else message.retry_count + 1
            message.retry_after = retry_after
            return self._channel.basic_publish(
                exchange='',
                routing_key=self._queue_name,
                body=json.dumps(message.to_json()),
                properties=pika.BasicProperties(delivery_mode=2))
        raise Exception("Channel is not set")
