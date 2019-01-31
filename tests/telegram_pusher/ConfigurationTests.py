from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock, call
from shared.configuration.configuration_parser import Parser
from shared.configuration.configuration_factory import ConfigurationFactory


class ConfigurationTests(TestCase):
    def test_configuration(self):
        from shared.configuration.implementations.configuration import QueueConfiguration

        a = QueueConfiguration()
        b = a.server


    @patch('shared.configuration.configuration_parser.ConfigParser')
    def test_configuration_parser_constructor(self, configuration_parser: Mock):
        configuration_parser.return_value = 'a'
        _parser = Parser('some_name')
        self.assertIsNotNone(_parser)
        configuration_parser.assert_called_once()
        self.assertEqual('some_name', _parser._file_name)

    @patch('shared.configuration.configuration_parser.open')
    def test_configuration_parser_parse_empty_file_name(self, open_file: Mock):
        with self.assertRaises(Exception) as _exception:
            _parser = Parser(None)
            _parser.parse()

        self.assertEqual(_exception.exception.args[0], "File name is empty")
        open_file.assert_not_called()

    @patch('shared.configuration.configuration_parser.open')
    @patch('shared.configuration.configuration_parser.ConfigParser')
    def test_configuration_parser_parse(self, config_parser: Mock, open_file: Mock):
        _file = MagicMock()
        _file.__exit__.return_value = None
        open_file.return_value = _file
        _config_parser_mock = Mock()
        _config_parser_mock.read_file.return_value = 'Ok'
        config_parser.return_value = _config_parser_mock

        _parser = Parser('aaaa')
        _parser.parse()

        config_parser.assert_called_once()
        open_file.assert_called_once_with('aaaa')
        _config_parser_mock.read_file.assert_called_once()
        _file.__exit__.assert_called_once()

    @patch('shared.configuration.configuration_parser.ConfigParser')
    def test_configuration_parser_get_value_no_dot(self, config_parser: Mock):
        _config_parser_mock = MagicMock()
        _config_parser_mock.__getitem__.return_value = 'Ok'
        config_parser.return_value = _config_parser_mock

        _parser = Parser('aaaa')
        # we skip _parser.parse here

        self.assertEqual('Ok', _parser.get_value('ddd'))
        _config_parser_mock.__getitem__.assert_called_once_with('ddd')

    @patch('shared.configuration.configuration_parser.ConfigParser')
    def test_configuration_parser_get_value(self, config_parser: Mock):
        _second_index = MagicMock()
        _second_index.__getitem__.return_value = 'Ok'
        _config_parser_mock = MagicMock()
        _config_parser_mock.__getitem__.return_value = _second_index
        config_parser.return_value = _config_parser_mock

        _parser = Parser('aaaa')
        # we skip _parser.parse here

        self.assertEqual('Ok', _parser.get_value('ddd.bbb'))
        _config_parser_mock.__getitem__.assert_called_once_with('ddd')
        _second_index.__getitem__.assert_called_once_with('bbb')

    @patch('shared.configuration.configuration_parser.ConfigParser')
    def test_configuration_parser_get_value_three_dots(self, config_parser: Mock):
        _second_index = MagicMock()
        _second_index.__getitem__.return_value = 'Ok'
        _config_parser_mock = MagicMock()
        _config_parser_mock.__getitem__.return_value = _second_index
        config_parser.return_value = _config_parser_mock

        _parser = Parser('aaaa')
        # we skip _parser.parse here

        with self.assertRaises(Exception) as _exception:
            _parser.get_value('ddd.bbb.cccc')

        self.assertEqual(_exception.exception.args[0],
                         "Path length has to be no longer than 2")
        _config_parser_mock.__getitem__.assert_not_called()
        _second_index.__getitem__.assert_not_called()

    @patch('shared.configuration.configuration_factory.Parser')
    @patch('shared.configuration.configuration_factory.impl.Configuration')
    def test_configuration_factory(self, configuration_mock: Mock, parser_mock: Mock):
        _parser = Mock()
        _parser.parse.return_value = None
        parser_mock.return_value = _parser
        configuration_mock.return_value = 'parsed'
        _factory = ConfigurationFactory.createConfiguration(
            'a_directory', 'dev')
        self.assertEqual('parsed', _factory)
        _parser.parse.assert_called_once()
        parser_mock.assert_called_once_with('a_directory/dev.ini')
        configuration_mock.assert_called_once_with(_parser)

    def test_configuration_parameters(self):
        _parser_mock = Mock()
        _parser_mock.get_value.side_effect = [
            'super_queue_server',
            '2050',
            'super_messages_queue',
            'super_errors_queue'
        ]
        _configuration = Configuration(_parser_mock)

        self.assertEqual('super_queue_server', _configuration.queueServer)
        self.assertEqual(2050, _configuration.queuePort)
        self.assertEqual('super_messages_queue',
                         _configuration.messagesQueueName)
        self.assertEqual('super_errors_queue', _configuration.errorsQueueName)

        self.assertEqual(4, _parser_mock.get_value.call_count)
        self.assertEqual([
            call('queue.queueServer'),
            call('queue.queuePort'),
            call('queue.messagesQueueName'),
            call('queue.errorsQueueName'),
        ], _parser_mock.get_value.call_args_list)
