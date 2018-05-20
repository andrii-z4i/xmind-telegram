from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from src.controllers.implementations.MessageRegistrar import MessageRegistrar
from pymysql.cursors import DictCursor


class MessageRegistrarTest(TestCase):
    sql = "INSERT INTO `messages` (`message`, `time`) VALUES (\"%s\", %f)"

    def setUp(self) -> None:
        _connection: MagicMock = MagicMock()
        _connection.close.return_value = None
        self._connection: Mock = _connection

    @patch("src.controllers.implementations.MessageRegistrar.pymysql.connect")
    def test_constructor_creates_connection(self, connect: Mock):
        connect.return_value = self._connection
        _registrar: MessageRegistrar = MessageRegistrar('a', 'b', 'c', 'd')
        self.assertEqual(_registrar._sql, MessageRegistrarTest.sql)
        self.assertEqual(_registrar._connection, self._connection)
        del _registrar
        connect.assert_called_once_with(charset='utf8mb4', cursorclass=DictCursor, db='b', host='a', password='d', user='c')
        self._connection.close.assert_called_once()

    @patch("src.controllers.implementations.MessageRegistrar.datetime")
    @patch("src.controllers.implementations.MessageRegistrar.pymysql.connect")
    def test_store_message(self, connect: Mock, dt: Mock):
        _cursor: MagicMock = MagicMock()
        self._connection.return_value = _cursor
        self._connection.commit.return_value = None
        connect.return_value = self._connection

        dt.utcnow.return_value.timestamp.return_value = 666.555
        _registrar: MessageRegistrar = MessageRegistrar('a', 'b', 'c', 'd')
        _registrar.store_message("Strange message")
        connect.return_value.__enter__.return_value.execute.assert_called_once_with(
            'INSERT INTO `messages` (`message`, `time`) VALUES ("Strange message", 666.555000)')
        connect.return_value.__exit__.assert_called_once()

