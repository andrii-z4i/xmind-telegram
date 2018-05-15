import src.controllers.interfaces as interfaces
from src.exceptions import BadResponseException
from src.model import Message, SentMessage, TelegramResponse
from src.exceptions.retry_exception import RetryException
from requests import post, Response
import json


class MessageSender(interfaces.MessageSender):
    def __init__(self, protocol: str, host: str, port: int, bot_key: str) -> None:
        super().__init__()
        self._url: str = f"{protocol}://{host}:{port}/bot{bot_key}/"

    def send_message(self, message: Message) -> SentMessage:
        url: str = f"{self._url}sendMessage"

        response: Response
        try:
            response = post(url, json=message.to_json())
        except Exception as e:
            print(e)
            raise BadResponseException('Can\'t send message')

        if not response.ok:
            raise BadResponseException('Bad response')

        r: dict = json.loads(response.content.decode('utf-8'))
        telegram_response = TelegramResponse(r)
        if telegram_response.success:
            return telegram_response.result

        if telegram_response.parameters.retry_after:
            raise RetryException(telegram_response.parameters.retry_after)

        raise BadResponseException('We got a bad response')
