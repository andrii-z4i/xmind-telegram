import argparse
from threading import Thread, Event

from app.acceptor import app
from app.rest_api import api, configure_rest_api
from app.acceptor_configuration.configuration_factory import ConfigurationFactory

from app.controllers.implementations.MessageHolder import MessageHolder
from app.controllers.implementations.Mediator import Mediator
from controllers.implementations.ErrorQueuePusher import ErrorQueuePusher
from controllers.implementations.ProcessorQueuePusher import ProcessorQueuePusher


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--environment', type=str, help="docker/dev", required=True)

    return parser.parse_args()


if __name__ == '__main__':
    event = Event()
    message_holder = MessageHolder(event)
    args = parse_args()
    configuration = ConfigurationFactory.createConfiguration(args.environment)
    configure_rest_api(api, configuration, message_holder)
    _kwargs = {'host': configuration.host,
               'port': configuration.port,
               'debug': configuration.debug,
               'use_debugger': configuration.use_debugger,
               'use_reloader': configuration.use_reloader}
    app_thread = Thread(target=app.run, name='app_thread', kwargs=_kwargs)

    processor_queue_pusher = ProcessorQueuePusher(queue_server=configuration.queueServer,
                                                  queue_port=configuration.queuePort,
                                                  queue_name=configuration.processorQueueName)
    error_queue_pusher = ErrorQueuePusher(queue_server=configuration.queueServer, queue_port=configuration.queuePort,
                                          queue_name=configuration.errorsQueueName)

    mediator = Mediator(event, message_holder, processor_queue_pusher, error_queue_pusher)
    mediator_thread = Thread(target=mediator.start, name='mediator_thread')
    #app_thread.run()
    mediator_thread.start()  # todo: understand is run() -correct choise or start() should be used
    app_thread.run()
    # app.run(
    #     host=acceptor_configuration.host,
    #     port=acceptor_configuration.port,
    #     debug=acceptor_configuration.debug,
    #     use_debugger=acceptor_configuration.use_debugger,
    #     use_reloader=acceptor_configuration.use_reloader)
    # message_holder = MessageHolder()
    # mediator = Mediator()
    print('end')
