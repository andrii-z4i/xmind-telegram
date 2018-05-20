from jsonobject import JsonObject, IntegerProperty, StringProperty


class Message(JsonObject):

    chat_id = IntegerProperty(required=True)
    text = StringProperty(required=True)


