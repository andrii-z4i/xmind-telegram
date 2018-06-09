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
from src.configuration.logging_configuration import create_logger, Logger, configure_logger, log_exception
from os import getcwd


class GracefulKiller:
    kill_now = False

    def __init__(self):
        self.logger: Logger = create_logger('GracefulKiller')
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum: int, frame: Any) -> None:
        self.logger.debug(f"Got a signal {signum} at frame {frame}")
        self.kill_now = True


class RunningParameters(object):
    def __init__(self, directory_path, environment='dev'):
        super().__init__()
        self.logger: Logger = create_logger("RunningParameters")
        if not directory_path:
            self.logger.debug('Directory path can\'t be empty')
            raise Exception('Directory path can\'t be empty')

        if not environment or not environment in ['dev', 'prod']:
            self.logger.debug(
                'Environment has to be set to either \'dev\' or \'prod\'')
            raise Exception(
                'Environment has to be set to either \'dev\' or \'prod\'')

        self.logger.debug(
            f"Directory path: {directory_path}, environment: {environment}")
        self._directory_path = directory_path
        self._environment = environment

    @property
    def configuration_directory(self) -> str:
        self.logger.debug(
            f"Get property configuration_directory - {self._directory_path}")
        return self._directory_path

    @property
    def environment(self) -> str:
        self.logger.debug(f"Get property environment - {self._environment}")
        return self._environment


def get_arguments() -> RunningParameters:
    logger: Logger = create_logger("ArgumentsParser")
    argumentParser = ArgumentParser(
        prog="Telegram pusher",
        usage="Provide all required parameters.",
        description="This is an entry point for a telegram pusher component which is the part of Telegram Bot",
        epilog="Ensure that your database has already set up a table to store not sent messages. Visit: https://goo.gl/yx7ryY"
    )
    argumentParser.add_argument('-d', '--directory', type=str, required=True)
    argumentParser.add_argument(
        '-e', '--environment', type=str, choices=['dev', 'prod'], required=True)
    logger.debug("Parse arguments")
    argumets = argumentParser.parse_args()
    runningParameters: RunningParameters = RunningParameters(
        argumets.directory, argumets.environment)
    return runningParameters


def prepare_processor(parameters: RunningParameters) -> interfaces.QueueProcessor:
    logger: Logger = create_logger("PrepareProcessor")
    logger.debug("create configuration")
    configuration: Configuration = ConfigurationFactory.createConfiguration(
        parameters.configuration_directory,
        parameters.environment)
    logger.debug("create queue channel")
    queueChannel: QueueChannel = QueueChannel(
        configuration.queueServer,
        configuration.queuePort,
        configuration.messagesQueueName
    )
    queueChannel.declare_queue()  # TODO: maybe move it out of this method
    logger.debug("create message sender")
    messageSender: MessageSender = MessageSender(
        configuration.telegramProtocol,
        configuration.telegramHost,
        configuration.telegramPort,
        configuration.telegramBotKey
    )
    logger.debug("create message registrar")
    messageRegistrar: MessageRegistrar = MessageRegistrar(
        configuration.databaseHost,
        configuration.databaseName,
        configuration.databaseUser,
        configuration.databasePassword
    )
    logger.debug("create queue pusher")
    queuePusher: QueuePusher = QueuePusher(
        configuration.queueServer,
        configuration.queuePort,
        configuration.messagesQueueName
    )
    logger.debug("create queue processor")
    queueProcessor: QueueProcessor = QueueProcessor(
        queueChannel,
        messageSender,
        messageRegistrar,
        queuePusher
    )
    return queueProcessor


if __name__ == '__main__':
    configure_logger("telegram-pusher")
    logger: Logger = create_logger("main")
    logger.info("Running in %s" % getcwd())
    try:
        parameters = get_arguments()
        queueProcessor: interfaces.QueueProcessor = prepare_processor(
            parameters)
        killer = GracefulKiller()
        logger.debug("start queue processor")
        queueProcessor.start()
    except Exception as ex:
        log_exception(ex)
        exit(-1)

    while True:
        time.sleep(1)
        logger.debug("Working...")
        if killer.kill_now:
            logger.debug("kill now...")
            break
    logger.debug("stop queue processor")
    queueProcessor.stop()
    logger.debug("exit")
