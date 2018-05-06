import pika

import controllers.interfaces as interfaces
from model import MessageContainer


class QueuePusher(interfaces.QueuePusher):

    def __init__(self, queue_server: str, queue_port: int, queue_name: str):
        super().__init__()
        self._queue_name = queue_name
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(queue_server, queue_port))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue_name, durable=True)

    def __del__(self):
        if self._connection:
            self._connection.close()

    def put_message_to_queue(self, message: MessageContainer, retry_after: int) -> bool:
        if self._channel:
            message.retry_after = retry_after
            return self._channel.basic_publish(
                exchange='',
                routing_key=self._queue_name,
                body=message.to_json(),  # TODO: check if it is enough to do to_json()
                properties=pika.BasicProperties(delivery_mode=2))
        raise Exception("Channel is not set")
