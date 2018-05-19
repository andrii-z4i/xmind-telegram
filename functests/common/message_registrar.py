from typing import List

import pymysql


class MessageRegistrar(object):
    def __init__(self, host: str, db: str, user: str, password: str) -> None:
        self._connection = pymysql.connect(
            host=host,
            db=db,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        connection = getattr(self, "_connection", None)
        if connection:
            connection.close()

    def remove_all_messages(self) -> None:
        sql: str = "DELETE FROM `messages`"
        with self._connection as _cursor:
            _cursor.execute(sql)

    def get_all_message(self) -> List[dict]:
        sql: str = "SELECT * FROM `messages`"
        with self._connection as _cursor:
            _cursor.execute(sql)
        return _cursor.fetchall()
