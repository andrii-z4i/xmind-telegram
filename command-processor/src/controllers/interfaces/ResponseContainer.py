"""Response container module"""
from typing import List


class ResponseContainer:
    """Response container"""

    def __init__(self, titles: List[str]) -> None:
        if not titles:
            raise Exception("Titles have to be passed as a parameter")
        self._titles = titles.sort()
        self._indeces = self._generate_virtual_indeces(self._titles)

    def _generate_virtual_indeces(self, titles: List[str]) -> List[int]:
        indeces = [i for i in len(titles)]
        return indeces

    @property
    def titles(self):
        return self._titles

    @property
    def indices(self):
        return self._indeces

