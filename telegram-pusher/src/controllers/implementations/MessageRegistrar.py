import json
import pymysql
import src.controllers.interfaces as interfaces
from src.model import MessageContainer
from datetime import datetime
import re


class MessageRegistrar(interfaces.MessageRegistrar):
    def __init__(self, host: str, db: str, user: str, password: str) -> None:
        self._connection = pymysql.connect(
            host=host,
            db=db,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        self._sql = "INSERT INTO `messages` (`message`, `time`) VALUES (\"%s\", %f)"

    def __del__(self):
        self._connection.close()

    def store_message(self, message: MessageContainer) -> None:
        with self._connection.cursor() as _cursor:
            _message_str = re.escape(json.dumps(message.to_json()))
            _cursor.execute(self._sql % (_message_str,  datetime.utcnow().timestamp()))
        self._connection.commit()
