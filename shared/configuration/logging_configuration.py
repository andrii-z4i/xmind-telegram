import logging as lg
from logging import Logger
import datetime
from os import mkdir
from os.path import exists, isdir
import traceback

__all__ = [
    'Logger',
    'configure_logger',
    'create_logger',
    'log_exception'
]

if not exists('./logs'):
    mkdir('./logs')
elif not isdir('./logs'):
    raise Exception(
        'No directory logs for storing logs, remove file with a similar name')

configured: bool = False


def configure_logger(logFile: str = None) -> None:
    FORMAT = '[%(name)s - %(levelname)s] %(asctime)-15s: %(message)s'
    now = datetime.datetime.now()
    if not logFile:
        fileNameToStoreLogs = now.strftime('%Y-%m-%d_%H-%M-%S')
    else:
        fileNameToStoreLogs = logFile

    lg.basicConfig(format=FORMAT, level=lg.DEBUG,
                   filename='./logs/%s.log' % fileNameToStoreLogs)
    lg.basicConfig(format=FORMAT, level=lg.DEBUG)
    configured = True


def create_logger(name: str) -> Logger:
    if not configured:
        configure_logger()
    return lg.getLogger(name)


def log_exception(exception: Exception, logger: Logger = None, log_level: int = 2) -> None:
    """
        <b>brief</b>: Logs exception using logger or creates new if not provided
        <b>param</b>: log_level := {0: logger.info, 1: logger.debug, 2: logger.error}
    """
    if not logger:
        logger = create_logger('NO_LOGGER')
    log_levels = {0: logger.info, 1: logger.debug, 2: logger.error}
    logger_func = logger.error
    if log_level in log_levels:
        logger_func = log_levels[log_level]
    logger_func(str(exception))
    logger_func(''.join(traceback.format_tb(exception.__traceback__)))
