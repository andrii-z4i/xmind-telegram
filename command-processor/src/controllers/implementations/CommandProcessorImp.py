import model
from ..interfaces.CommandProcessor import CommandProcessor
from ..interfaces.BaseCommandProcessor import BaseCommandProcessor
from .FileCommandsProcessor import FileCommandsProcessor
from .SheetCommandsProcessor import SheetCommandsProcessor
from .TopicCommandsProcessor import TopicCommandsProcessor


class CommandProcessorImpl(CommandProcessor):
    """docstring for CommandProcessor"""

    def __init__(self, arg):
        super(CommandProcessorImpl, self).__init__()
        self.arg = arg
        self._file_commands_processor: BaseCommandProcessor = FileCommandsProcessor()
        self._sheet_commands_processor: BaseCommandProcessor = \
            SheetCommandsProcessor()
        self._topic_commands_processor: BaseCommandProcessor = TopicCommandsProcessor()

    def process(self, message: model.SentMessage) -> bool:
        raise NotImplementedError()

    @property
    def file_commands(self) -> BaseCommandProcessor:
        return self._file_commands_processor

    @property
    def sheet_commands(self) -> BaseCommandProcessor:
        return self._sheet_commands_processor
    
    @property
    def topic_commands(self) -> BaseCommandProcessor:
        return self._topic_commands_processor