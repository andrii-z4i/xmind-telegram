from jsonobject import JsonObject, BooleanProperty, ObjectProperty, StringProperty
from src.model.SentMessage import SentMessage
from src.model.ResponseParameters import ResponseParameters


class TelegramResponse(JsonObject):

    success = BooleanProperty(name='ok')
    result = ObjectProperty(SentMessage)
    description = StringProperty()
    parameters = ObjectProperty(ResponseParameters)
