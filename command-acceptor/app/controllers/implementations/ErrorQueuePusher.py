import json
import pika
import src.controllers.interfaces as interfaces
from model import ErrorMessageContainer
from configuration.logging_configuration import create_logger, Logger, log_exception


class ErrorQueuePusher(interfaces.QueuePusher):

    def __init__(self, queue_server: str, queue_port: int, queue_name: str) -> None:
        super().__init__()
        self.logger: Logger = create_logger("QueuePusher")
        self.logger.debug(
            f"in __init__({queue_server}, {queue_port}, {queue_name})")
        self._queue_name = queue_name
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(queue_server, queue_port, connection_attempts=3, retry_delay=5))
        self._channel = self._connection.channel()

    def __del__(self):
        self.logger.debug("in __del__")
        _connection = getattr(self, "_connection", None)
        if _connection and _connection.is_open:
            self.logger.debug("close connection")
            _connection.close()

    def put_message_to_queue(self, message: ErrorMessageContainer, retry_after: int) -> bool:
        self.logger.debug("in put message to queue")
        self.logger.debug(
            f"Message: {message.to_json()}, retry_after: {retry_after}")
        if self._channel:
            message.retry_count = 1 if not message.retry_count else message.retry_count + 1
            message.retry_after = retry_after
            self.logger.debug("Before publish")
            return self._channel.basic_publish(
                exchange='',
                routing_key=self._queue_name,
                body=json.dumps(message.to_json()),
                properties=pika.BasicProperties(delivery_mode=2))
        self.logger.error("channel is not set")
        raise Exception("Channel is not set")
