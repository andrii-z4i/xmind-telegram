import app.controllers.interfaces as interfaces
from app.models.AcceptedMessage import AcceptedMessage
import json


class CommandFactory(interfaces.CommandFactory):
    def __init__(self, message: AcceptedMessage) -> None:
        self._text = AcceptedMessage.text
        self._user_id = AcceptedMessage.from_field.user_id
        self._language = AcceptedMessage.from_field.language_code

    # def split_input(self) -> list:
    #     return self._text.split()

    def command_values(self) -> dict:
        values_list = self._text.split()
        values_dict = {'operation': values_list[0], 'subject':values_list[1], 'value':''} # Maybe None will be better than empty strng
        if len(values_list) > 2:
            values_dict['value'] = ' '.join(values_list[2:])
        return values_dict

    def get_commands_dict(self) -> dict:
        with open('./configuration/commands_dict.json') as f:
            data = json.load(f)
        return data

    def validate_operation(self, operation: str, commands_dict: dict, language: str) -> str:
        #lngs_list = [language]
        for key, value in commands_dict[language]['operation'].items():
            if operation in value:
                return key
        if language != 'en-US':
            for key, value in commands_dict['en-US']['operation'].items():
                if operation in value:
                    return key

    def prepare_command(self):
        pass


