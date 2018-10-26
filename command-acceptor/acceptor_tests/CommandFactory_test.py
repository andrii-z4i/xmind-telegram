from acceptor_tests.base import Base
from unittest import TestCase
from unittest.mock import patch, Mock
from model.AcceptedMessage import AcceptedMessage
from model.Command import Command
from app.controllers.implementations.CommandFactory import CommandFactory
import json


class CommandFactoryTests(Base):
    _d = {"message_id": 35,
          "from": {
              "id": 430810000,
              "is_bot": False,
              "first_name": "Mykola",
              "last_name": "Pysarev",
              "language_code": "en-US"
          },
          "chat": {
              "id": 430816986,
              "first_name": "Mykola",
              "last_name": "Pysarev",
              "type": "private"
          },
          "date": 1523450921,
          "text": "hello"}

    _predefined_message = AcceptedMessage(_d)

    def test_excessive_parameters(self):
        _element = CommandFactory(self._predefined_message)

        _parameters = [
            ('__init__', 1),
            ('_prepare_error_message', 1),
            ('_command_values', 0),
            ('_get_commands_dict', 0),
            ('get_data_by_language', 2),
            ('validate_word', 2),
            ('validate_command', 2),
            ('prepare_command', 0)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

    def test_init_with_correct_message(self):
        # Run
        self._predefined_message.text = "hello"
        _factory = CommandFactory(self._predefined_message)

        # Check
        self.assertEqual(_factory._text, "hello")
        self.assertEqual(_factory._user_id, 430810000)
        self.assertEqual(_factory._language, "en-US")

    def test_init_with_incorrect_parameter(self):
        # Run
        with self.assertRaises(AttributeError) as err:
            _factory = CommandFactory('wrong_format_message')

        # Check
        self.assertEqual(repr(err.exception), repr(AttributeError("'str' object has no attribute 'text'")))

    def test_prepare_error_message_with_correct_parameter(self):
        # Prepare
        _factory = CommandFactory(self._predefined_message)
        _values_dict = {
            "operation": {
                "create": ["create", "crate", "crete", "crt"],
                "delete": ["delete", "dlete", "dlt"],
                "add": ["add", "ad"],
                "get": ["get", "gt"]
            },
            "subject": {
                "node": ["node", "nod", "nd"],
                "topic": ["topic", "tpic", "topc", "tpc"],
                "sheet": ["sheet", "shet", "sht"],
                "file": ["file", "fle", "fil"]
            }
        }
        _exp_message = "The command 'hello' has incorrect format. Command should contain an operation_name, " \
                       "a subject_name and pointer. F.e. create file temp.txt. Available operations are: " \
                       "['create', 'delete', 'add', 'get']; availabel subjects are ['node', 'topic', 'sheet', 'file']"
        # Run
        _result = _factory._prepare_error_message(_values_dict)

        # Check
        self.assertEqual(_result, _exp_message)

    # INTEGRATION TESTS
    @patch('app.controllers.implementations.CommandFactory.CommandFactory._get_commands_dict')
    def test_valid_cases_validation(self, get_command_dict: Mock):
        get_command_dict.return_value = {
            "en-US": {
                "operation": {
                    "create": ["create", "crate", "crete", "crt"],
                    "delete": ["delete", "dlete", "dlt"],
                    "add": ["add", "ad"],
                    "get": ["get", "gt"]
                },
                "subject": {
                    "node": ["node", "nod", "nd"],
                    "topic": ["topic", "tpic", "topc", "tpc"],
                    "sheet": ["sheet", "shet", "sht"],
                    "file": ["file", "fle", "fil"]
                }
            }
        }
        _user_id = self._predefined_message.from_field.user_id
        _input_dict = dict(
            [('create node', Command(operation='create', subject='node', identifier=None, owner=_user_id)),
             ('file delete', Command(operation='delete', subject='file', identifier=None, owner=_user_id)),
             ('child node create', Command(operation='create', subject='node', identifier='child', owner=_user_id)),
             ('create child node', Command(operation='create', subject='node', identifier='child', owner=_user_id)),
             ('add node child', Command(operation='add', subject='node', identifier='child', owner=_user_id)),
             ('create new child node',
              Command(operation='create', subject='node', identifier='new child', owner=_user_id)),
             ('node delete learn best practice',
              Command(operation='delete', subject='node', identifier='learn best practice', owner=_user_id)),
             ('add very topic big', Command(operation='add', subject='topic', identifier='very big', owner=_user_id))])

        for _text, _command_to_compare in _input_dict.items():
            # prepare
            self._predefined_message.text = _text
            _factory = CommandFactory(self._predefined_message)

            # Run
            _result = _factory.prepare_command()

            # Check
            self.assertEqual(_result, _command_to_compare)

    @patch('app.controllers.implementations.CommandFactory.CommandFactory._get_commands_dict')
    def test_exceptional_cases_validation(self, get_command_dict: Mock):
        get_command_dict.return_value = {
            "en-US": {
                "operation": {
                    "create": ["create", "crate", "crete", "crt"],
                    "delete": ["delete", "dlete", "dlt"],
                    "add": ["add", "ad"],
                    "get": ["get", "gt"]
                },
                "subject": {
                    "node": ["node", "nod", "nd"],
                    "topic": ["topic", "tpic", "topc", "tpc"],
                    "sheet": ["sheet", "shet", "sht"],
                    "file": ["file", "fle", "fil"]
                }
            }
        }
        _input_list = ['operation no subject create',
                       'operation two subjects create topic node',
                       'subject no operation nod',
                       'subject two operations create node delete']

        for _text in _input_list:
            # prepare
            self._predefined_message.text = _text
            _factory = CommandFactory(self._predefined_message)

            # Run
            with self.assertRaises(Exception) as e:
                _result = _factory.prepare_command()

            # Check
            self.assertEqual(repr(e.exception), repr(Exception(
                "The command '{}' has incorrect format. Command should contain an operation_name, a subject_name and pointer. F.e. create file temp.txt. Available operations are: ['create', 'delete', 'add', 'get']; availabel subjects are ['node', 'topic', 'sheet', 'file']".format(
                    _text))))
