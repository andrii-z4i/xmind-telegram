class RetryException(Exception):
    def __init__(self, retry_after: int) -> None:
        super().__init__(retry_after, None)
        self._retry_after: int = retry_after

    @property
    def retry_after(self) -> int:
        return self._retry_after
