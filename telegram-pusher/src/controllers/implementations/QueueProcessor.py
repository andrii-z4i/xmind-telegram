import json
import re
from threading import Thread
import src.controllers.interfaces as interfaces
from src.exceptions import BadResponseException
from src.exceptions import RetryException
from model import MessageContainer
from configuration.logging_configuration import create_logger, Logger, log_exception


class QueueProcessor(interfaces.QueueProcessor):
    def __init__(
            self,
            queue_channel: interfaces.QueueChannel,
            message_sender: interfaces.MessageSender,
            message_registrar: interfaces.MessageRegistrar,
            queue_pusher: interfaces.QueuePusher
    ) -> None:
        self.logger: Logger = create_logger("QueueProcessor")
        self.logger.debug("in __init__")
        self._message_sender: interfaces.MessageSender = message_sender
        self._message_registrar: interfaces.MessageRegistrar = message_registrar
        self._queue_pusher: interfaces.QueuePusher = queue_pusher
        self._channel: interfaces.QueueChannel = queue_channel
        self._channel.set_inner_message_processor(self.process_event)
        self._thread = Thread(
            target=lambda x: x._channel.start_consuming(), args=(self,))

    def process_event(self, body: dict) -> None:
        self.logger.debug("in process event for body=%s" % str(body))
        _message: MessageContainer = None
        try:
            _message = MessageContainer(body)
            self._message_sender.send_message(_message.message)
        except RetryException as _ex:
            self.logger.debug(
                f"got retry order after {_ex.retry_after} seconds")
            if not self._queue_pusher.put_message_to_queue(_message, _ex.retry_after):
                self.logger.error(
                    f"can't put message to queue")
                self._message_registrar.store_message(_message)
        except Exception as ex2:
            log_exception(ex2, self.logger)
            _message_str = re.escape(json.dumps(body))
            self._message_registrar.store_message(_message_str)

    def start(self) -> None:
        self.logger.debug("in start")
        self._channel.activate_consumer()
        self._thread.start()

    def stop(self) -> None:
        self.logger.debug("in stop")
        self._channel.deactivate_consumer()
        self._thread.join()
