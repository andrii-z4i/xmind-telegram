from jsonobject import JsonObject, IntegerProperty, StringProperty


class Command(JsonObject):
    operation = StringProperty()
    subject = StringProperty()
    name = StringProperty()
    virtual_id = IntegerProperty()
    user_id = IntegerProperty()
    chat_id = IntegerProperty()

    def __eq__(self, other):
        return self.operation == other.operation and self.subject == other.subject and self.name == other.name and self.virtual_id == other.virtual_id and self.user_id == other.user_id and self.chat_id == other.chat_id
