import app.controllers.interfaces as interfaces
from model.AcceptedMessage import AcceptedMessage
from model.MessageToProcessor import MessageToProcessor
from model.Command import Command
import json


class CommandFactory(interfaces.CommandFactory):
    def __init__(self, message: AcceptedMessage) -> None:
        self._text = message.text
        self._user_id = message.from_field.user_id  # should we validate id on here or just send it to the processor?
        self._language = message.from_field.language_code

    def _prepare_error_message(self, data_by_language: dict)-> str:
        _error_message_text = "The command '{}' has incorrect format. Command should contain an operation_name, a subject_name and pointer. F.e. create file temp.txt. Available operations are: {}; availabel subjects are {}"
        _operations = list(data_by_language['operation'].keys())
        _subjects = list(data_by_language['subject'].keys())
        _err_message = _error_message_text.format(self._text, _operations, _subjects)
        return _err_message

    def _command_values(self) -> list:
        values_list = self._text.split()
        if len(values_list) < 2: #todo: think will we have real cases with just operation and subject
            raise Exception
        return values_list

    def _get_commands_dict(self) -> dict:
        with open('./configuration/commands_dict.json') as f:  # todo: path to the file should be imported as parameter
            data = json.load(f)
        return data

    def get_data_by_language(self, language: str, data_dict: dict) -> dict:
        if language in data_dict:
            return data_dict[language]
        else:
            return data_dict['en-US']

    def validate_word(self, word: str, possible_values: dict) -> str:
        for key, value in possible_values.items():
            if word in value:
                return key

    def validate_command(self, words: list, possible_values: dict) -> dict:
        _operation_list = []
        _subject_list = []
        _identifiers_list = []
        _result = dict()
        for word in words:
            if self.validate_word(word, possible_values['operation']):
                _operation_list.append(word)
            elif self.validate_word(word, possible_values['subject']):
                _subject_list.append(word)
            else:
                _identifiers_list.append(word)

        if len(_operation_list) != 1 or len(_subject_list) != 1:
            raise Exception(self._prepare_error_message(possible_values))

        _result['operation'] = _operation_list[0]
        _result['subject'] = _subject_list[0]
        _result['identifier'] = None
        if _identifiers_list:
            _result['identifier'] = ' '.join(_identifiers_list)
        return _result

    def prepare_command(self):
        _command_values = self._command_values()
        _command_dict = self._get_commands_dict()
        _data_by_language = self.get_data_by_language(self._language, _command_dict)
        _validation_result = self.validate_command(_command_values, _data_by_language)
        _command = Command(operation=_validation_result['operation'], subject=_validation_result['subject'],
                           identifier=_validation_result['identifier'], owner=self._user_id)

        return _command
