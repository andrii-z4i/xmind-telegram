class DependencyInjection(object):
    def __init__(self):
        super(DependencyInjection, self).__init__()
        self._queue = None

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, value):
        self._queue = value

dependencies = DependencyInjection()
