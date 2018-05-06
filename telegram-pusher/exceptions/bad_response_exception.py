class BadResponseException(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason, None)
        self._reason: str = reason

    @property
    def reason(self) -> str:
        return self._reason
