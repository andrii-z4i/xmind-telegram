from flask_restful import Resource, reqparse
from flask import request
import pika
from app.controllers.implementations.RequestAnalyser import RequestAnalyser
from app.controllers.implementations.CommandFactory import CommandFactory
from app.models.ErrorMessage import ErrorMessage
from app.dependencies import dependencies

parser = reqparse.RequestParser()
#parser.add_argument('result')


class UserController(Resource):
    def __init__(self, message_holder, *args, **kwargs):
        super(UserController, self).__init__(*args, **kwargs)
        self._queue = dependencies.queue
        self.message_holder = message_holder

    def get(self):
        status = self._queue.add('someValue')
        return {'status': status}, 200

    def post(self):
        try:
            _json = request.json
            _analyser = RequestAnalyser(_json)
            _accepted_message = _analyser.process
            self.message_holder.put(_accepted_message)
            return 200

        except Exception as err:
            # _err_message: ErrorMessage = ErrorMessage(bad_request=_json)
            # _err_message.error_text = 'Failed to extract json from request: "{}"'.format(err.args[0])
            # todo: send error message and send/return bad? response
            return 400
