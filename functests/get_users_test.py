from unittest import TestCase
import mockserver as mk

class GetUsersTest(TestCase):

    def test_http_requests(self):
        _client = mk.MockServerClient("http://localhost:1080")
        _client.expect(mk.request("GET", "/user"), mk.response(200, "I'm here"), mk.times(2))
