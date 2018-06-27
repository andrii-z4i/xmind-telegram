from unittest import TestCase

from app.controllers.implementations.RequestAnalyser import RequestAnalyser
from model.AcceptedMessage import AcceptedMessage


class RequestAnalyserTests(TestCase):

    def test_init_process_with_good_request(self):
        # Prepare
        _d = {"message_id": 35,
              "from": {
                  "id": 430816986,
                  "is_bot": False,
                  "first_name": "Mykola",
                  "last_name": "Pysarev",
                  "language_code": "en-US"
              },
              "chat": {
                  "id": 430816986,
                  "first_name": "Mykola",
                  "last_name": "Pysarev",
                  "type": "private"
              },
              "date": 1523450921,
              "text": "hello"}

        _message_to_compare = AcceptedMessage(_d)


        # Run
        _analyser = RequestAnalyser(_d)
        _result = _analyser.process

        # Check
        self.assertEqual(_analyser._request_dict, _d)

        self.assertEqual(_message_to_compare.from_field.user_id, _result.from_field.user_id)
        self.assertEqual(_result.from_field.first_name, _result.from_field.first_name)
        self.assertEqual(_result.from_field.is_bot, _result.from_field.is_bot)
        self.assertEqual(_result.from_field.language_code, _result.from_field.language_code)
        #self.assertEqual(_test_user, _result.from_field) todo: think about adding __eq__ method to models

        self.assertEqual( _message_to_compare.chat.chat_id, _result.chat.chat_id)
        self.assertEqual( _message_to_compare.chat.type, _result.chat.type)

        self.assertEqual(_result.message_id, 35)
        self.assertEqual(_result.text, "hello")

        # self.assertEqual(_result,_message_to_compare )

    def test_init_process_bad_request(self):
        # Prepare
        # Message without text item
        _d = {"message_id": 35,
              "from": {
                  "id": 430816986,
                  "is_bot": False,
                  "first_name": "Mykola",
                  "last_name": "Pysarev",
                  "language_code": "en-US"
              },
              "chat": {
                  "id": 430816986,
                  "first_name": "Mykola",
                  "last_name": "Pysarev",
                  "type": "123"
              },
              "date": 1523450921}

        # Run
        _analyser = RequestAnalyser(_d)
        with self.assertRaises(Exception) as _ex:
            _result = _analyser.process

        # Check
        self.assertNotEqual(_ex.exception.args[0].find("'123' not in choices:"), -1)

    def test_init_process_no_values_request(self):
        # Prepare

        # Message without text item
        _d = {"message_id": 35,
              "from": {
                  "id": 430816986,
                  "is_bot": False,
                  "first_name": "Mykola",
                  "last_name": "Pysarev",
                  "language_code": "en-US"
              },
              "chat": {
                  "id": 430816986,
                  "first_name": "Mykola",
                  "last_name": "Pysarev",
                  "type": "private"
              },
              "date": 1523450921}

        # Run
        _analyser = RequestAnalyser(_d)

        with self.assertRaises(Exception) as _ex:
            _result = _analyser.process

        # Check
        self.assertNotEqual(_ex.exception.args[0].find("text is required"), -1)


    # def test_init_request_without_json(self):
    #     # Prepare
    #     _request = Mock()
    #     _json = PropertyMock(side_effect=Exception('test'))
    #     type(_request).json = _json
    #
    #
    #     # Run
    #     _analyser = RequestAnalyser(_request)
    #
    #     # Check
    #     self.assertEqual(_analyser._err_message.error_text, 'Failed to extract json from request: "test"')






