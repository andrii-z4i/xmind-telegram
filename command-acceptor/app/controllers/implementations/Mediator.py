import app.controllers.interfaces as interfaces
from app.controllers.implementations.MessageHolder import MessageHolder
from app.controllers.implementations.CommandFactory import CommandFactory
from model.AcceptedMessage import AcceptedMessage
from model.Command import Command
from model.ErrorMessage import ErrorMessage
from threading import Event
from app.controllers.implementations.ProcessorQueuePusher import ProcessorQueuePusher
from app.controllers.implementations.ErrorQueuePusher import ErrorQueuePusher
from model.SentMessageContainer import SentMessageContainer
from model.ErrorMessageContainer import ErrorMessageContainer


class Mediator(interfaces.Mediator):
    def __init__(self, event: Event, message_holder: MessageHolder, processor_queue_pusher: ProcessorQueuePusher,
                 error_queue_pusher: ErrorQueuePusher) -> None:
        self.active: bool = False
        self.event = event
        self.message_holder = message_holder
        self.processor_queue_pusher = processor_queue_pusher
        self.error_queue_pusher = error_queue_pusher

    # def is_busy(self) -> bool:
    #     return self.busy

    def start(self) -> None:
        self.active = True
        while self.active:
            if self.event.wait():
                while not self.message_holder.isEmpty and self.active:
                    _message: AcceptedMessage = self.message_holder.get()
                    factory: CommandFactory = CommandFactory(_message)
                    try:
                        command: Command = factory.prepare_command()
                        command_message_container = SentMessageContainer(message=command.to_json(), message_type='response')
                        self.processor_queue_pusher.put_message_to_queue(message=command_message_container, retry_after=2) #todo: do we need to check the response (true, false)
                        # place where command should be send to the queue
                    except Exception as e:
                        error_message_container = SentMessageContainer(message=e.args[0], message_type='error')
                        self.error_queue_pusher.put_message_to_queue(message=error_message_container, retry_after=2)
                        pass

                self.event.clear()

    def stop(self) -> None:
        self.active = False  # todo: think how to improve this to stop Mediator imidiatly not to wait till the next check condition i While statement
