from jsonobject import JsonObject, IntegerProperty, StringProperty


class Message(JsonObject):

    chat_id = IntegerProperty()
    text = StringProperty()
