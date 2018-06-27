from jsonobject import JsonObject, IntegerProperty, StringProperty


class Chat(JsonObject):
    chat_id = IntegerProperty(name='id', required=True)
    type = StringProperty(
        choices=['private', 'group', 'supergroup', 'channel'], required=True)
