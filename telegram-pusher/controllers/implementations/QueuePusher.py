import controllers.interfaces as interfaces
from model import Message


class QueuePusher(interfaces.QueuePusher):
    def put_message_to_queue(self, message: Message, retry_after: int) -> bool:
        pass