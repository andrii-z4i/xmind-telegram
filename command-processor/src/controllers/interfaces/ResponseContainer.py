"""Response container module"""
from typing import List


class ResponseContainer:
    """Response container"""

    def __init__(self, titles: List[str]) -> None:
        if not titles:
            raise Exception("Titles have to be passed as a parameter")
        self._titles = titles.copy()
        self._titles.sort()
        self._indices = self._generate_virtual_indices(self._titles)

    def _generate_virtual_indices(self, titles: List[str]) -> List[int]:
        indeces = [i for i in range(len(titles))]
        return indeces

    @property
    def titles(self):
        return self._titles

    @property
    def indices(self):
        return self._indices

    def get_title_by_index(self, virtual_index: int) -> str:
        if virtual_index < 0 or virtual_index > len(self._titles):
            raise Exception('Index is out of range')
        return self._titles[virtual_index]
