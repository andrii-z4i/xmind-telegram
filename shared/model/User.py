from jsonobject import JsonObject, IntegerProperty, BooleanProperty, StringProperty


class User(JsonObject):

    user_id = IntegerProperty(name='id')
    is_bot = BooleanProperty()
    first_name = StringProperty()
    language_code = StringProperty()
