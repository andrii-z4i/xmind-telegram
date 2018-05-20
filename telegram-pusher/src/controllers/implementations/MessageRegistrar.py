import json
import pymysql
import src.controllers.interfaces as interfaces
from src.model import MessageContainer
from datetime import datetime
import re
from src.configuration.logging_configuration import create_logger, Logger, log_exception


class MessageRegistrar(interfaces.MessageRegistrar):
    def __init__(self, host: str, db: str, user: str, password: str) -> None:
        self.logger: Logger = create_logger("MessageRegistrar")
        self.logger.debug("in init")
        self._connection = pymysql.connect(
            host=host,
            db=db,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        self._sql = "INSERT INTO `messages` (`message`, `time`) VALUES (\"%s\", %f)"

    def __del__(self):
        self.logger.debug("in __del__")
        connection = getattr(self, "_connection", None)
        if connection:
            self.logger.debug("close connection")
            connection.close()

    def store_message(self, message_body: str) -> None:
        self.logger.debug("store message %s" % message_body)
        with self._connection as _cursor:
            _cursor.execute(self._sql %
                            (message_body,  datetime.utcnow().timestamp()))
            self.logger.debug("message stored")
