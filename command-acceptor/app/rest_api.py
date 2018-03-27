from flask_restful import Api
from app.acceptor import app
from app.controller.user_controller import UserController
from app.dependencies import dependencies
from app.rabbitmq_queue import RabbitMqQueue

api = Api(app)

def configure_rest_api(api, configuration):
    dependencies.queue = RabbitMqQueue(configuration.queueServer, configuration.queuePort, configuration.queueName)
    api.add_resource(UserController, '/v1/user')


