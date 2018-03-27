from threading import Event
from queue_consumer import ConsumerQueue
from unittest import TestCase
from requests import get


class TestAcceptor(TestCase):
    def test_v1_get_user(self):
        e = Event()
        q = ConsumerQueue('queue', e, 'localhost', 1082)
        q.start()
        r = get('http://localhost:1081/v1/user')
        print(r.json())
        wait_result = e.wait(100)
        v = q.get_last_value()
        print(v)
        q.stop()