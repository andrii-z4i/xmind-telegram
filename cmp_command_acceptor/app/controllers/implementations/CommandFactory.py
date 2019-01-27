from cmp_command_acceptor.app.controllers import interfaces
from shared.model.AcceptedMessage import AcceptedMessage
from shared.model.MessageToProcessor import MessageToProcessor
from shared.model.Command import Command
import json


class CommandFactory(interfaces.CommandFactory):
    def __init__(self, message: AcceptedMessage) -> None:
        self._text = message.text
        self._user_id = message.from_field.user_id  # should we validate id on here or just send it to the processor?
        self._chat_id = message.chat.chat_id
        self._language = message.from_field.language_code

    def _prepare_error_message(self, data_by_language: dict)-> str:
        _error_message_text = 'The command "{}" has incorrect format. Command should contain an operation_name, a subject_name, subject_id or name of the new entity. (F.e. create file "<name>"; select topic 23...). Available operations are: {}; availabel subjects are {}'
        _operations = list(data_by_language['operation'].keys())
        _subjects = list(data_by_language['subject'].keys())
        _err_message = _error_message_text.format(self._text, _operations, _subjects)
        return _err_message

    def _create_validation(self, data_by_language_dict):  #todo: seems like create validation should go first as only it check for " . Think how to avoid strict order
        _result = dict()
        _brackets_count = self._text.count('"')
        if _brackets_count == 2:
            _result['name'] = self._text[self._text.find('"')+1: self._text.rfind('"')]
            _command_rest = self._text[0:self._text.find('"')] + self._text[self._text.rfind('"')+1:]
            _command_list = _command_rest.split()
            if len(_command_list) not in [1, 2]:
                raise Exception
            for i in _command_list:
                if i in data_by_language_dict['operation']['create']:
                    _result['operation'] = 'create'
                    _command_list.remove(i)
                    break
            if not _result['operation']:
                raise Exception

            _result['subject'] = None
            if _command_list:
                for key, value in data_by_language_dict['subject'].items():
                    if _command_list[0] in value:
                        _result['subject'] = key
                        break
                if not _result['subject']:
                    raise Exception
        return _result

    def _delete_validation(self, data_by_language_dict):
        _result = dict()
        _command_list = self._text.split()
        if len(_command_list) not in [2, 3]:
            raise Exception
        for i in data_by_language_dict['operation']['delete']:
            if i in _command_list:
                _result['operation'] = 'delete'
                _command_list.remove(i)
                break
        if not _result:
            return _result
        if len(_command_list) == 2:
            for key, value in data_by_language_dict['subject'].items():
                for i in _command_list:
                    if i in value:
                        _result['subject'] = key
                        _command_list.remove(i)
                        break
            if 'subject' not in _result.keys():
                raise Exception
        try:
            _result['id'] = int(_command_list[0])
        except:
            raise Exception
        return _result

    def _select_validation(self, data_by_language_dict):  #todo: delete and select looks same - should this be unit somehow?
        _result = dict()
        _command_list = self._text.split()
        if len(_command_list) not in [2, 3]:
            return _result
        for i in data_by_language_dict['operation']['select']:
            if i in _command_list:
                _result['operation'] = 'select'
                _command_list.remove(i)
                break
        if not _result:
            return _result
        if len(_command_list) == 2:
            for key, value in data_by_language_dict['subject'].items():
                for i in _command_list:
                    if i in value:
                        _result['subject'] = key
                        _command_list.remove(i)
                        break
            if 'subject' not in _result.keys():
                raise Exception
        try:
            _result['id'] = int(_command_list[0])
        except:
            raise Exception
        return _result

    def _list_validation(self, data_by_language_dict):
        _result = dict()
        _command_list = self._text.split()
        for i in data_by_language_dict['operation']['list']:
            if i in _command_list:
                _result['operation'] = 'list'
                _command_list.remove(i)
                break
        if not _result:
            return _result
        if len(_command_list) > 1:
            raise Exception
        if _command_list:
            for key, value in data_by_language_dict['subject'].items():
                if _command_list[0] in value:
                    _result['subject'] = key
                    _command_list.remove(_command_list[0])
                    break
            if 'subject' not in _result.keys():
                raise Exception
        return _result

    def _get_commands_dict(self) -> dict:
        with open('./cmp_command_acceptor/configuration/commands_dict.json') as f:  # todo: path to the file should be imported as parameter
            data = json.load(f)
        return data

    def get_data_by_language(self, language: str, data_dict: dict) -> dict:
        if language in data_dict:
            return data_dict[language]
        else:
            return data_dict['en-US']

    def prepare_command(self):
        _command = Command(user_id=self._user_id, chat_id=self._chat_id)
        _command_dict = self._get_commands_dict()
        _data_by_language = self.get_data_by_language(self._language, _command_dict)
        try:
            _validation_result = self._create_validation(_data_by_language)
            if _validation_result:
                _command.operation = _validation_result['operation']
                _command.subject = _validation_result['subject']
                _command.name = _validation_result['name']
                _command.virtual_id = None
                return _command
            _validation_result = self._select_validation(_data_by_language)
            if _validation_result:
                _command.operation = _validation_result['operation']
                _command.virtual_id = _validation_result['id']
                if 'subject' in _validation_result.keys():
                    _command.subject = _validation_result['subject']
                else:
                    _command.subject = None
                _command.name = None
                return _command
            _validation_result = self._list_validation(_data_by_language)
            if _validation_result:
                _command.operation = _validation_result['operation']
                if 'subject' in _validation_result.keys():
                    _command.subject = _validation_result['subject']
                else:
                    _command.subject = None
                _command.name = None
                _command.virtual_id = None
                return _command
            _validation_result = self._delete_validation(_data_by_language)
            if _validation_result:
                _command.operation = _validation_result['operation']
                _command.virtual_id = _validation_result['id']
                if 'subject' in _validation_result.keys():
                    _command.subject = _validation_result['subject']
                else:
                    _command.subject = None
                _command.name = None
                return _command
            else:
                raise Exception('Command is not valid!')
        except:
            raise Exception({'chat_id': self._chat_id, 'text': self._prepare_error_message(_data_by_language)})
