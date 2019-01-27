from tests.command_acceptor.base import Base
from unittest import TestCase
from unittest.mock import patch, Mock
from shared.model.AcceptedMessage import AcceptedMessage
from shared.model.Command import Command
from cmp_command_acceptor.app.controllers.implementations.CommandFactory import CommandFactory
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
            # ('_command_values', 0),
            ('_create_validation', 1),
            ('_delete_validation', 1),
            ('_list_validation', 1),
            ('_select_validation', 1),
            ('_get_commands_dict', 0),
            ('get_data_by_language', 2),
            # ('validate_word', 2),
            # ('validate_command', 2),
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
                "create":["create", "crate", "crete", "crt"],
                "delete":["delete", "dlete", "dlt"],
                "select":["select", "slect", "selct", "slct", "selekt"],
                "list":["list", "lst", "lis"]
            },
            "subject": {
                "topic":["topic", "topics", "tpic", "topc", "tpc"],
                "sheet":["sheet", "sheets", "shet", "sht"],
                "file":["file", "files", "fle", "fil"]
            }
        }
        _exp_message = """The command "hello" has incorrect format. Command should contain an operation_name, a subject_name, subject_id or name of the new entity. (F.e. create file "<name>"; select topic 23...). Available operations are: ['create', 'delete', 'select', 'list']; availabel subjects are ['topic', 'sheet', 'file']"""

        # Run
        _result = _factory._prepare_error_message(_values_dict)

        # Check
        self.assertEqual(_result, _exp_message)

    # INTEGRATION TESTS
    # @patch('app.controllers.implementations.CommandFactory.CommandFactory._get_commands_dict')
    # def test_valid_cases_validation(self, get_command_dict: Mock):
    def test_valid_cases_validation(self):
        # get_command_dict.return_value = {
        #     "en-US": {
        #         "operation": {
        #             "create": ["create", "crate", "crete", "crt"],
        #             "delete": ["delete", "dlete", "dlt"],
        #             "add": ["add", "ad"],
        #             "get": ["get", "gt"]
        #         },
        #         "subject": {
        #             "node": ["node", "nod", "nd"],
        #             "topic": ["topic", "tpic", "topc", "tpc"],
        #             "sheet": ["sheet", "shet", "sht"],
        #             "file": ["file", "fle", "fil"]
        #         }
        #     }
        # }
        _user_id = self._predefined_message.from_field.user_id
        _chat_id = self._predefined_message.chat.chat_id
        _input_dict = dict(
            [('create file "file name"',
              Command(operation='create', subject='file', name='file name', virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('topic crete "topic name"',
              Command(operation='create', subject='topic', name='topic name', virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('"First Try" sheet create',
              Command(operation='create', subject='sheet', name='First Try', virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('creat "entity name"',
              Command(operation='create', subject=None, name='entity name', virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('delete 23',
              Command(operation='delete', subject=None, name=None, virtual_id=23, user_id=_user_id, chat_id=_chat_id)),
             ('12 file delet',
              Command(operation='delete', subject='file', name=None, virtual_id=12, user_id=_user_id, chat_id=_chat_id)),
             ('shet 11 delete',
              Command(operation='delete', subject='sheet', name=None, virtual_id=11, user_id=_user_id, chat_id=_chat_id)),
             ('topics del 44',
              Command(operation='delete', subject='topic', name=None, virtual_id=44, user_id=_user_id, chat_id=_chat_id)),
             ('select 33',
              Command(operation='select', subject=None, name=None, virtual_id=33, user_id=_user_id, chat_id=_chat_id)),
             ('file 34 slct',
              Command(operation='select', subject='file', name=None, virtual_id=34, user_id=_user_id, chat_id=_chat_id)),
             ('35 tpc selekt',
              Command(operation='select', subject='topic', name=None, virtual_id=35, user_id=_user_id, chat_id=_chat_id)),
             ('selct sheets 36',
              Command(operation='select', subject='sheet', name=None, virtual_id=36, user_id=_user_id, chat_id=_chat_id)),
             ('list',
              Command(operation='list', subject=None, name=None, virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('list files',
              Command(operation='list', subject='file', name=None, virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('sheets list',
              Command(operation='list', subject='sheet', name=None, virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('list topic',
              Command(operation='list', subject='topic', name=None, virtual_id=None, user_id=_user_id, chat_id=_chat_id)),
             ('topics list',
              Command(operation='list', subject='topic', name=None, virtual_id=None, user_id=_user_id, chat_id=_chat_id))])

        for _text, _command_to_compare in _input_dict.items():
            # prepare
            self._predefined_message.text = _text
            _factory = CommandFactory(self._predefined_message)

            # Run
            _result = _factory.prepare_command()

            # Check
            self.assertEqual(_result, _command_to_compare)
    #
    # @patch('app.controllers.implementations.CommandFactory.CommandFactory._get_commands_dict')
    # def test_exceptional_cases_validation(self, get_command_dict: Mock):
    #     get_command_dict.return_value = {
    #         "en-US": {
    #             "operation": {
    #                 "create": ["create", "crate", "crete", "crt"],
    #                 "delete": ["delete", "dlete", "dlt"],
    #                 "add": ["add", "ad"],
    #                 "get": ["get", "gt"]
    #             },
    #             "subject": {
    #                 "node": ["node", "nod", "nd"],
    #                 "topic": ["topic", "tpic", "topc", "tpc"],
    #                 "sheet": ["sheet", "shet", "sht"],
    #                 "file": ["file", "fle", "fil"]
    #             }
    #         }
    #     }
    #     _input_list = ['operation no subject create',
    #                    'operation two subjects create topic node',
    #                    'subject no operation nod',
    #                    'subject two operations create node delete']
    #
    #     for _text in _input_list:
    #         # prepare
    #         self._predefined_message.text = _text
    #         _factory = CommandFactory(self._predefined_message)
    #
    #         # Run
    #         with self.assertRaises(Exception) as e:
    #             _result = _factory.prepare_command()
    #
    #         # Check
    #         self.assertEqual(repr(e.exception), repr(Exception({'chat_id': 430816986,
    #                                                             'text': "The command '{}' has incorrect format. Command should contain an operation_name, a subject_name and pointer. F.e. create file temp.txt. Available operations are: ['create', 'delete', 'add', 'get']; availabel subjects are ['node', 'topic', 'sheet', 'file']".format(
    #                                                                 _text)})))
