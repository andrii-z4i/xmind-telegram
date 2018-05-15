import signal
from argparse import ArgumentParser, Namespace
import time
from typing import Any

from src.configuration.configuration_factory import ConfigurationFactory
from src.configuration.interfaces.configuration import Configuration
from src.controllers.implementations.MessageRegistrar import MessageRegistrar
from src.controllers.implementations.MessageSender import MessageSender
from src.controllers.implementations.QueueChannel import QueueChannel
from src.controllers.implementations.QueueProcessor import QueueProcessor
from src.controllers.implementations.QueuePusher import QueuePusher
import src.controllers.interfaces as interfaces


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum: int, frame: Any) -> None:
        self.kill_now = True


class RunningParameters(object):
    def __init__(self, directory_path, environment='dev'):
        super().__init__()
        if not directory_path:
            raise Exception('Directory path can\'t be empty')

        if not environment or not environment in ['dev', 'prod']:
            raise Exception('Environment has to be set to either \'dev\' or \'prod\'')

        self._directory_path = directory_path
        self._environment = environment

    @property
    def configuration_directory(self) -> str:
        return self._directory_path

    @property
    def environment(self) -> str:
        return self._environment


def get_arguments() -> RunningParameters:
    argumentParser = ArgumentParser(
        prog="Telegram pusher",
        usage="Provide all required parameters.",
        description="This is an entry point for a telegram pusher component which is the part of Telegram Bot",
        epilog="Ensure that your database has already set up a table to store not sent messages. Visit: https://goo.gl/yx7ryY"
    )
    argumentParser.add_argument('-d', '--directory', type=str, required=True)
    argumentParser.add_argument('-e', '--environment', type=str, choices=['dev', 'prod'], required=True)
    argumets = argumentParser.parse_args()
    runningParameters: RunningParameters = RunningParameters(argumets.directory, argumets.environment)
    return runningParameters


def prepare_processor(parameters: RunningParameters) -> interfaces.QueueProcessor:
    configuration: Configuration = ConfigurationFactory.createConfiguration(
        parameters.configuration_directory,
        parameters.environment)
    queueChannel: QueueChannel = QueueChannel(
        configuration.queueServer,
        configuration.queuePort,
        configuration.messagesQueueName
    )
    queueChannel.declare_queue() # TODO: maybe move it out of this method
    messageSender: MessageSender = MessageSender(
        configuration.telegramProtocol,
        configuration.telegramHost,
        configuration.telegramPort,
        configuration.telegramBotKey
    )
    messageRegistrar: MessageRegistrar = MessageRegistrar(
        configuration.databaseHost,
        configuration.databaseName,
        configuration.databaseUser,
        configuration.databasePassword
    )
    queuePusher: QueuePusher = QueuePusher(
        configuration.queueServer,
        configuration.queuePort,
        configuration.messagesQueueName
    )
    queueProcessor: QueueProcessor = QueueProcessor(
        queueChannel,
        messageSender,
        messageRegistrar,
        queuePusher
    )
    return queueProcessor


if __name__ == '__main__':
    parameters = get_arguments()
    queueProcessor: interfaces.QueueProcessor = prepare_processor(parameters)
    killer = GracefulKiller()
    queueProcessor.start()

    while True:
        time.sleep(1)
        print("Working...")
        if killer.kill_now:
            break
    queueProcessor.stop()
    print("It's time to say goodbye....")