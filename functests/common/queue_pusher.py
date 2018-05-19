import json
import pika


class QueuePusher(object):

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

    def put_message_to_queue(self, message: dict) -> bool:
        if self._channel:
            return self._channel.basic_publish(
                exchange='',
                routing_key=self._queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2))
        raise Exception("Channel is not set")
