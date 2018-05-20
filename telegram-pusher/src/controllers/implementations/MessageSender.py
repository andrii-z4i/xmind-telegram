import src.controllers.interfaces as interfaces
from src.exceptions import BadResponseException
from src.model import Message, SentMessage, TelegramResponse
from src.exceptions.retry_exception import RetryException
from requests import post, Response
import json
from src.configuration.logging_configuration import create_logger, Logger, log_exception


class MessageSender(interfaces.MessageSender):
    def __init__(self, protocol: str, host: str, port: int, bot_key: str) -> None:
        super().__init__()
        self.logger: Logger = create_logger("MessageSender")
        self._url: str = f"{protocol}://{host}:{port}/bot{bot_key}/"
        self.logger.debug("in __init__, url = %s" % self._url)

    def send_message(self, message: Message) -> SentMessage:
        self.logger.debug("send message %s", message)
        url: str = f"{self._url}sendMessage"

        response: Response
        try:
            response = post(url, json=message.to_json())
        except Exception as e:
            log_exception(e, self.logger)
            raise BadResponseException('Can\'t send message')

        if not response.ok:
            self.logger.debug("response ok = false")
            raise BadResponseException('Bad response')

        r: dict = json.loads(response.content.decode('utf-8'))
        telegram_response = TelegramResponse(r)
        if telegram_response.success:
            self.logger.debug("Telegram response success = True")
            return telegram_response.result

        if telegram_response.parameters.retry_after:
            self.logger.debug("response has retry after order")
            raise RetryException(telegram_response.parameters.retry_after)

        raise BadResponseException('We got a bad response')
