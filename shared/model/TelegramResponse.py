from jsonobject import JsonObject, BooleanProperty, ObjectProperty, StringProperty
from model.SentMessage import SentMessage
from model.ResponseParameters import ResponseParameters


class TelegramResponse(JsonObject):

    success = BooleanProperty(name='ok')
    result = ObjectProperty(SentMessage)
    description = StringProperty()
    parameters = ObjectProperty(ResponseParameters)
