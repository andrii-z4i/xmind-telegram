import model
from ..interfaces.CommandProcessor import CommandProcessor
from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from .FileCommandsProcessor import FileCommandsProcessor


class CommandProcessorImpl(CommandProcessor):
    """docstring for CommandProcessor"""

    def __init__(self, arg):
        super(CommandProcessorImpl, self).__init__()
        self.arg = arg
        self._file_commands_processor: BaseCommandProcessor = FileCommandsProcessor()

    def process(self, message: model.SentMessage) -> bool:
        raise NotImplementedError()

    @property
    def file_commands(self) -> BaseCommandProcessor:
        return self._file_commands_processor
