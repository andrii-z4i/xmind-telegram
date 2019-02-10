from jsonobject import JsonObject, IntegerProperty, ObjectProperty
from shared.model.Chat import Chat
from shared.model.User import User


class SentMessage(JsonObject):

    message_id = IntegerProperty()
    from_field = ObjectProperty(User, name='from')
    date = IntegerProperty()
    chat = ObjectProperty(Chat)
