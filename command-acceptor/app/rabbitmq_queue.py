from abc import ABC, abstractmethod

import pika


class IQueue(ABC):
    @abstractmethod
    def add(self, value):
        return NotImplemented


class RabbitMqQueue(IQueue):
    def __init__(self, queue_server, queue_port=5672, queue_name='someQueue'):
        super(RabbitMqQueue, self).__init__()
        self._queue_name = queue_name
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(queue_server, queue_port))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue_name)

    def __del__(self):
        if self._connection:
            self._connection.close()

    def add(self, value):
        if self._channel:
            return self._channel.basic_publish(exchange='',
                              routing_key=self._queue_name,
                              body=value)
        raise Exception("Channel is not set")

    def get(self):
        if self._channel:
            return self._channel.basic_get(self._queue_name, no_ack=False)
        raise Exception("Channel is not set")
