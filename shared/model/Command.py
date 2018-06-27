from jsonobject import JsonObject, IntegerProperty, StringProperty


class Command(JsonObject):

    operation_type = StringProperty()
    operation_subject = StringProperty()
    subject_identifier = StringProperty()
    operation_owner = IntegerProperty()  # User id
