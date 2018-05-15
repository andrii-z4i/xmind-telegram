import json
from typing import Callable
import src.controllers.interfaces as interfaces
from pika import BlockingConnection, ConnectionParameters


class QueueChannel(interfaces.QueueChannel):

    def __init__(self, host: str, port: int, queue_name: str) -> None:
        super().__init__()
        self._queue_name = queue_name
        self._connection = BlockingConnection(
            ConnectionParameters(host, port))
        self._channel = self._connection.channel()
        self._consumer_tag: str = None
        self._callback: Callable[[dict], None] = None

    def __del__(self):
        _connection = getattr(self, "_connection", None)
        if _connection and _connection.is_open:
            _connection.close()

    def declare_queue(self) -> None:
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        self._channel.basic_qos(prefetch_count=1)

    def set_inner_message_processor(self, callback: Callable[[dict], None]) -> None:
        self._callback = callback

    def activate_consumer(self) -> None:
        self._consumer_tag = self._channel.basic_consume(
            self._inner_processing, queue=self._queue_name)
        self._channel.start_consuming()

    def deactivate_consumer(self) -> None:
        self._channel.stop_consuming(self._consumer_tag)

    def _inner_processing(self, ch, method, properties, body):
        # FIXME: We have to use logger here
        print(
            f"got body -> >>{body}<< on channel '{ch}' using method '{method}' with properties '{properties}'")
        _body_dict: dict = json.loads(body.decode('utf-8'))
        self._callback(_body_dict)
        ch.basic_ack(delivery_tag=method.delivery_tag)
