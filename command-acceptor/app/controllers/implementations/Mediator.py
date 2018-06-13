import app.controllers.interfaces as interfaces
from app.controllers.implementations.MessageHolder import MessageHolder
from app.controllers.implementations.CommandFactory import CommandFactory
from app.models.AcceptedMessage import AcceptedMessage
from app.models.Command import Command
from threading import Event


class Mediator(interfaces.Mediator):
    def __init__(self, event: Event, message_holder: MessageHolder)-> None:
        self.busy: bool = False
        self.event = event
        self.message_holder = message_holder

    # def is_busy(self) -> bool:
    #     return self.busy

    def start(self)-> None:
        self.busy = True
        while self.busy:
            if self.event.wait():
                while not self.message_holder.isEmpty():
                    _message: AcceptedMessage = self.message_holder.get()
                    factory: CommandFactory = CommandFactory(_message)
                    command: Command = factory.prepare_command()
                    #place where command should be send to the queue

                self.event.clear()

    def stop(self)-> None:
        self.busy = False  # todo: think how to improve this to stop Mediator imidiatly not to wait till the next check condition i While statement
