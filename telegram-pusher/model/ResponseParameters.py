from jsonobject import JsonObject, IntegerProperty


class ResponseParameters(JsonObject):
    migrate_to_chat_id = IntegerProperty()
    retry_after = IntegerProperty()  # TODO: THIS PARAMETER HAS TO BE TAKEN INTO ACCOUNT
