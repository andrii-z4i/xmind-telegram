from jsonobject import JsonObject, IntegerProperty, ObjectProperty, StringProperty


class MessageToProcessor(JsonObject):

    operation_type = StringProperty(required=True)
    operation_subject = StringProperty(required=True)
    operation_owner = IntegerProperty(required=True)
    operation_pointer = StringProperty()
