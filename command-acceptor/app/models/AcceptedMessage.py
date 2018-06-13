from jsonobject import JsonObject, IntegerProperty, ObjectProperty, StringProperty
from app.models.Chat import Chat
from app.models.User import User


class AcceptedMessage(JsonObject):

    message_id = IntegerProperty(required=True)
    from_field = ObjectProperty(User, name='from', required=True)
    date = IntegerProperty()
    chat = ObjectProperty(Chat, required=True)
    text = StringProperty(required=True)
