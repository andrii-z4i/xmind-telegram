from threading import Thread
import pika

class ConsumerQueue(object):
    def __init__(self, name, event, host, port):
        super(ConsumerQueue, self).__init__()
        self._name = name
        self._event = event
        self._received_values = []
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._name)
        self._consumer_tag = self._channel.basic_consume(
            self._queue_callback, queue=self._name, no_ack=True)
        self._thread = Thread(target=lambda x: x._channel.start_consuming(), args=(self,))


    def __del__(self):
        if self._connection:
            self._connection.close()

    def _queue_callback(self, ch, method, properties, body):
        self._received_values.append({'ch': ch, 'method': method, 'properties': properties, 'body': body})
        self._event.set()

    def get_last_value(self):
        return self._received_values.pop()

    def start(self):
        self._thread.start()

    def stop(self):
        self._channel.stop_consuming(self._consumer_tag)
        self._thread.join()
