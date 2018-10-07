class UserObject(object):
    """User's abstract"""

    def __init__(self, user_id: str):
        if not user_id or not len(user_id):
            raise Exception('UserId has to be a valid string')

        self._user_id: str = user_id
        self._user_working_dir: str = None

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def working_dir(self) -> str:
        return self._user_working_dir

    @working_dir.setter
    def working_dir(self, working_dir: str) -> None:
        if not working_dir:
            raise Exception('Path should be set')

        self._user_working_dir = working_dir
