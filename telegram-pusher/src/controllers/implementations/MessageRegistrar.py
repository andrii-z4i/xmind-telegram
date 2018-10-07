import json
import pymysql
import src.controllers.interfaces as interfaces
from model import MessageContainer
import re
from configuration.logging_configuration import create_logger, Logger, log_exception


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
        self._sql = "INSERT INTO `messages` (`message`, `time`) VALUES (\"%s\", now())"

    def __del__(self):
        self.logger.debug("in __del__")
        connection = getattr(self, "_connection", None)
        if connection:
            self.logger.debug("close connection")
            connection.close()

    def store_message(self, message_body: str) -> None:
        self.logger.debug("store message %s" % message_body)
        with self._connection as _cursor:
            self.logger.debug("Execute")
            _sql: str = self._sql % message_body
            self.logger.debug(_sql)
            _cursor.execute(_sql)
            self.logger.debug("message stored")
