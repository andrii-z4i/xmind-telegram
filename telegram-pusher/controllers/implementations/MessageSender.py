import controllers.interfaces as interfaces
from model import Message, SentMessage, TelegramResponse
from exceptions.retry_exception import RetryException
from requests import post, Response
import json


class MessageSender(interfaces.MessageSender):
    def __init__(self, protocol: str, host: str, port: int, bot_key: str, queue_pusher: interfaces.QueuePusher) -> None:
        super().__init__()
        self._url: str = f"{protocol}://{host}:{port}/bot{bot_key}/"
        self._queue_pusher: interfaces.QueuePusher = queue_pusher

    def send_message(self, message: Message) -> SentMessage:
        url: str = f"{self._url}sendMessage"

        response: Response = post(url, json=message.to_json())
        if not response.ok:
            raise Exception('Bad response')

        r: dict = json.loads(response.content.decode('utf-8'))
        telegram_response = TelegramResponse(r)
        if telegram_response.success:
            return telegram_response.result

        if telegram_response.parameters.retry_after:
            self._queue_pusher.put_message_to_queue(
                message, telegram_response.parameters.retry_after)
            raise RetryException(telegram_response.parameters.retry_after)

        raise Exception('We got a bad response')
