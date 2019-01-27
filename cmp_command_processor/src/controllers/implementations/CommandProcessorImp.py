from shared import model
from cmp_command_processor.src.controllers.interfaces.CommandProcessor import CommandProcessor
from cmp_command_processor.src.controllers.interfaces.BaseCommandProcessor import BaseCommandProcessor
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
        self._subject_map = {
            'file': self.file_commands,
            'sheet': self.sheet_commands,
            'topic': self.topic_commands
        }

    def process(self, message: model.Command) -> bool:
        processor: BaseCommandProcessor = self._subject_map[message.subject]
        _operation = message.operation
        _result = True
        if _operation == 'create':
            processor.create(message.user_id, message.name)
        elif _operation == 'delete':
            processor.delete(message.user_id, message.virtual_id)
        elif _operation == 'select':
            processor.select(message.user_id, message.virtual_id)
        elif _operation == 'list':
            _response = processor.list(message.user_id)
            # TODO: send to the queue response
        elif _operation == 'current':
            _response = processor.current(message.user_id)
            # TODO: send to the queue response
        else:
            # strange
            raise Exception('Operation is not supported')
        return _result

    @property
    def file_commands(self) -> BaseCommandProcessor:
        return self._file_commands_processor

    @property
    def sheet_commands(self) -> BaseCommandProcessor:
        return self._sheet_commands_processor
    
    @property
    def topic_commands(self) -> BaseCommandProcessor:
        return self._topic_commands_processor