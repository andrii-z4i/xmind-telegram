import json
from typing import Callable
import src.controllers.interfaces as interfaces
from pika import BlockingConnection, ConnectionParameters
from shared.configuration.logging_configuration import create_logger, Logger, log_exception


class QueueChannel(interfaces.QueueChannelInterface):

    def __init__(self, host: str, port: int, queue_name: str) -> None:
        super().__init__()
        self.logger: Logger = create_logger("QueueChannel")
        self.logger.debug(f"in __init__({host}, {port}, {queue_name})")
        self._queue_name = queue_name
        self._connection = BlockingConnection(
            ConnectionParameters(host, port, connection_attempts=3, retry_delay=5))
        self._channel = self._connection.channel()
        self._consumer_tag: str = None
        self._callback: Callable[[dict], None] = None

    def __del__(self):
        self.logger.debug("in __del__")
        _connection = getattr(self, "_connection", None)
        if _connection and _connection.is_open:
            self.logger.debug("close connection")
            _connection.close()

    def declare_queue(self) -> None:
        self.logger.debug("in declare queue")
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        self._channel.basic_qos(prefetch_count=1)

    def set_inner_message_processor(self, callback: Callable[[dict], None]) -> None:
        self.logger.debug("in set inner message processor")
        self._callback = callback

    def activate_consumer(self) -> None:
        self.logger.debug("in activate consumer")
        self._consumer_tag = self._channel.basic_consume(
            self._inner_processing, queue=self._queue_name)
        self._channel.start_consuming()
        self.logger.debug(f"got consumer tag {self._consumer_tag}")

    def deactivate_consumer(self) -> None:
        self.logger.debug("in deactivate consumer")
        self._channel.stop_consuming(self._consumer_tag)

    def _inner_processing(self, ch, method, properties, body):
        self.logger.debug("in inner processing")
        self.logger.debug(
            f"got body -> >>{body}<< on channel '{ch}' using method '{method}' with properties '{properties}'")
        _body_dict: dict = json.loads(body.decode('utf-8'))
        self._callback(_body_dict)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.logger.debug("message acked")
