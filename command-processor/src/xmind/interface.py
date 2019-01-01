"""This module implements operations on xmind"""

from typing import List


class XmindOperations:
    """Returns nodes"""
    def add_node(self, xmind_object, node_title):
        """Returns nodes"""
        raise NotImplementedError()

    def remove_node(self, xmind_object, node_index):
        """Returns nodes"""
        raise NotImplementedError()

    def navigate_by_path(self, xmind_object, path) -> None:
        """Returns nodes"""
        raise NotImplementedError()

    def enumerate_nodes(self, xmind_object) -> List[str]:
        """Returns nodes"""
        raise NotImplementedError()
