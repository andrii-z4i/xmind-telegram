from xmind.core.loader import WorkbookLoader
from unittest import TestCase


class LoaderTest(TestCase):
    """Loader test"""

    def test_init_get_abs_path_throws(self):
        """test case when get_abs_path throws exception"""

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

