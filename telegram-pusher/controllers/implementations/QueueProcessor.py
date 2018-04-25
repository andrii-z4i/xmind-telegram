import controllers.interfaces as interfaces


class QueueProcessor(interfaces.QueueProcessor):
    def register_callback(self, call_back_method) -> None:
        pass

    def activate(self) -> None:
        pass

    def deactivate(self) -> None:
        pass
