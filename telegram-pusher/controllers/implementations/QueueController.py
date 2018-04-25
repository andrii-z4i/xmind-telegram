from model import Message
import controllers.interfaces as interfaces
from configuration.interfaces.configuration import Configuration
from threading import Thread, Event
from typing import List


class QueueController(object):
    def __init__(self, queue_channel: interfaces.QueueChannel, sync_object: Event) -> None:
        super().__init__()
        self._sync_object = sync_object
        self._received_values: List[Message] = []
        self._channel: interfaces.QueueChannel = queue_channel
        self._channel.set_callback_method(self._queue_callback)
        self._thread = Thread(
            target=lambda x: x._channel.start_consuming(), args=(self,))

    def _queue_callback(self, ch, method, properties, body):
        # FIXME: We have to use logger here
        print(
            f"got body -> >>{body}<< on channel '{ch}' using method '{body}' with properties '{properties}'")
        _body_dict: dict = json.loads(body.decode('utf-8'))
        _message = Message(_body_dict)
        self._received_values.append(_message)
        self._sync_object.set()

    def get_last_value(self):
        return self._received_values.pop()

    def start(self):
        self._channel.activate_consumer()
        self._thread.start()

    def stop(self):
        self._channel.stop_consuming()
        self._thread.join()
