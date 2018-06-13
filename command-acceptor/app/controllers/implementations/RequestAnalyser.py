from flask import request
# from controllers import interfaces
import app.controllers.interfaces as interfaces
from app.models.User import User
from app.models.Chat import Chat
from app.models.ErrorMessage import ErrorMessage
from app.models.AcceptedMessage import AcceptedMessage
from jsonobject import DictProperty


class RequestAnalyser(interfaces.RequestAnalyser):
    def __init__(self, request_dict: dict) -> None:
        self._request_dict = request_dict

    @property
    def process(self):
        _accepted_message: AcceptedMessage = AcceptedMessage(self._request_dict)
        # if not (_accepted_message.text and \
        #         _accepted_message.message_id and \
        #         _accepted_message.date and \
        #         _accepted_message.chat.chat_id and \
        #         _accepted_message.chat.type and \
        #         _accepted_message.from_field.first_name and \
        #         _accepted_message.from_field.user_id and \
        #         _accepted_message.from_field.is_bot is not None and \
        #         _accepted_message.from_field.language_code):

            # raise Exception('Mandatory value is missing')

        return _accepted_message

    # @property
    # def accepted_message(self) -> AcceptedMessage:
    #     if self._accepted_message:
    #         return self._acc_message
