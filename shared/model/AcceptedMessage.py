from jsonobject import JsonObject, IntegerProperty, ObjectProperty, StringProperty
from shared.model.Chat import Chat
from shared.model.User import User


class AcceptedMessage(JsonObject):

    message_id = IntegerProperty(required=True)
    from_field = ObjectProperty(User, name='from', required=True)
    date = IntegerProperty()
    chat = ObjectProperty(Chat, required=True)
    text = StringProperty(required=True)
