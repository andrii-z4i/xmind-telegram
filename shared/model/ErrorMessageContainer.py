from jsonobject import JsonObject, IntegerProperty, ObjectProperty, StringProperty
from shared.model.ErrorMessage import ErrorMessage


class ErrorMessageContainer(JsonObject):
    # retry section
    # Flow should be next
    # try to send message -> received response with retry_after -> put to queue back
    # and set retry_after and set create_time
    retry_after = IntegerProperty(exclude_if_none=True)
    create_time = IntegerProperty(exclude_if_none=True)
    retry_count = IntegerProperty(exclude_if_none=True)
    message_type = StringProperty(choices=['error', 'response'], required=True)
    message = ObjectProperty(ErrorMessage, required=True)