from jsonobject import JsonObject, IntegerProperty, ObjectProperty, StringProperty

from model import Message


class MessageContainer(JsonObject):
    # retry section
    # Flow should be next
    # try to send message -> received response with retry_after -> put to queue back
    # and set retry_after and set create_time
    retry_after = IntegerProperty()
    create_time = IntegerProperty()
    retry_count = IntegerProperty()
    message_type = StringProperty(choices=['error', 'response'])
    message = ObjectProperty(Message)