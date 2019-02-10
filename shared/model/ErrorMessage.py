from jsonobject import JsonObject, ObjectProperty, StringProperty, DictProperty
from flask import request
from shared.model.AcceptedMessage import AcceptedMessage


class ErrorMessage(JsonObject):

    error_text = StringProperty()
    bad_request = JsonObject()
