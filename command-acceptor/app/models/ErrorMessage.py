from jsonobject import JsonObject, ObjectProperty, StringProperty, DictProperty
from flask import request


class ErrorMessage(JsonObject):

    error_text = StringProperty()
    bad_request = DictProperty()
