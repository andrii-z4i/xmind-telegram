import unittest
from abc import abstractmethod
from unittest.mock import patch, Mock, MagicMock


class Base(unittest.TestCase):
    """Base class for any acceptor_tests"""

    def _test_method_by_excessive_parameters(self, pair, _element):
        _method_name_to_test = pair[0]
        _parameters_count = pair[1]
        _check_for_none = True

        if isinstance(_parameters_count, tuple):
            _p = _parameters_count
            _parameters_count = _p[0]
            _check_for_none = _p[1]

        _method_to_call = getattr(_element, _method_name_to_test)
        _call_method_with_parameters = [
            i for i in range(_parameters_count + 1)]
        # self.getLogger().debug("Test method '%s' with %d parameters",
        #                        _method_name_to_test, _parameters_count)
        with self.assertRaises(TypeError) as _ex:
            _method_to_call(*_call_method_with_parameters)

        # self.getLogger().debug("Got an exception: '%s'", _ex.exception.args[0])
        self.assertTrue(_ex.exception.args[0].find(
            "%s() takes" % _method_name_to_test) != -1)

        if _parameters_count > 0 and _check_for_none:  # Let's test with None as well
            # self.getLogger().debug(
            #     "Test method '%s' with 0 parameters", _method_name_to_test)
            with self.assertRaises(TypeError) as _exNone:
                _method_to_call()

            # self.getLogger().debug("Got an exception: '%s'",
            #                        _exNone.exception.args[0])
            self.assertTrue(_exNone.exception.args[0].find(
                "%s() missing" % _method_name_to_test) != -1)
