from jsonobject import JsonObject, BooleanProperty, ObjectProperty, StringProperty
from shared.model.SentMessage import SentMessage
from shared.model.ResponseParameters import ResponseParameters


class TelegramResponse(JsonObject):

    success = BooleanProperty(name='ok')
    result = ObjectProperty(SentMessage)
    description = StringProperty()
    parameters = ObjectProperty(ResponseParameters)
