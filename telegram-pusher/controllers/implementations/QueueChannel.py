import controllers.interfaces as interfaces
from pika import BlockingConnection, ConnectionParameters


class QueueChannel(interfaces.QueueChannel):

    def __init__(self, host: str, port: int, queue_name: str) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._queue_name = queue_name
        self._connection = BlockingConnection(
            ConnectionParameters(host, port))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue_name)
        self._consumer_tag: str = None

    def __del__(self):
        if self._connection:
            self._connection.close()

    def activate_consumer(self) -> None:
        self._consumer_tag = self._channel.basic_consume(
            self._callback, queue=self._queue_name, no_ack=True)

    def start_consuming(self) -> None:
        self._channel.start_consuming()

    def stop_consuming(self) -> None:
        self._channel.stop_consuming(self._consumer_tag)
