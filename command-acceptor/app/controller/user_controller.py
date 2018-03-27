from flask_restful import Resource
import pika

from app.dependencies import dependencies


class UserController(Resource):
    def __init__(self, *args, **kwargs):
        super(UserController, self).__init__(*args, **kwargs)
        self._queue = dependencies.queue

    def get(self):
        status = self._queue.add('someValue')
        return {'status': status }, 200