import src.controllers.interfaces as interfaces
import model


class CommandProcessor(interfaces.CommandProcessor):
    """docstring for CommandProcessor"""

    def __init__(self, arg):
        super(CommandProcessor, self).__init__()
        self.arg = arg

    def process(self, message: model.SentMessage) -> bool:
        raise NotImplementedError()

