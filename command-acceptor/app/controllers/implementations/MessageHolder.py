import app.controllers.interfaces as interfaces


class MessageHolder(interfaces.MessageHolder):
    def __init__(self, event):
        self.items = []
        self.event = event

    @property
    def isEmpty(self):
        return self.items == []
    is_empty = isEmpty

    def put(self, item):
        self.items.insert(0, item)
        # if not self.mediator.busy:
        #     self.mediator.start()
        self.event.set()
        print(2)

    def get(self):
        print(3)
        return self.items.pop()

    def size(self):
        print(4)
        return len(self.items)
