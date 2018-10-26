from jsonobject import JsonObject, IntegerProperty, StringProperty


class Command(JsonObject):
    operation = StringProperty()
    subject = StringProperty()
    identifier = StringProperty()
    owner = IntegerProperty()  # User id

    def __eq__(self, other):
        return self.operation == other.operation and self.subject == other.subject and self.identifier == other.identifier and self.owner == other.owner
