"""User object module"""


class UserObject:
    """User's abstract"""

    def __init__(self, user_id: str):
        """constructor"""
        if not user_id:
            raise Exception('UserId has to be a valid string')

        self._user_id: str = user_id
        self._user_working_dir: str = None

    def __str__(self) -> str:
        return f'{self.working_dir}/{self._user_id}'

    @property
    def user_id(self) -> str:
        """user id"""
        return self._user_id

    @property
    def working_dir(self) -> str:
        """working dir"""
        return self._user_working_dir

    @working_dir.setter
    def working_dir(self, working_dir: str) -> None:
        """working dir setter"""
        if not working_dir:
            raise Exception('Path should be set')

        self._user_working_dir = working_dir
