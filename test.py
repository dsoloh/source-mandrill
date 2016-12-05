import unittest

from mock import MagicMock
from mandrill import Users
from panoply_mandrill import PanoplyMandrill

OPTIONS = {
    "logger": lambda *args: None # don't log on test 
}

# get rid of the API validation check
Users.ping = MagicMock()

class TestMandrill(unittest.TestCase):

    def setUp(self):
        self.stream = PanoplyMandrill({
            "key": "MandrillKey"
        }, OPTIONS)

    def tearDown(self):
        pass

    def test_simple_request(self):
        metrics = [{ 
            "name":"tags",
            "path": "all_time_series",
            "category": "tags"
        }]
        res = [{'test': 'orange'}]
        self.stream.mandrill_client.tags.all_time_series = MagicMock(return_value=res)
        self.stream.metrics = metrics
        result = self.stream.read()[0]

        self.assertEqual(result.get("type"), "tags")
        self.assertEqual(result.get("key"), "MandrillKey")
        self.assertEqual(result.get("test"), "orange")
    
    def test_iterate_metrics(self):
        metrics = [{ 
            "name":"tags",
            "path": "all_time_series",
            "category": "tags"
        }, {
            "name":"webhooks",
            "path": "list",
            "category": "webhooks" 
        }]
        self.stream.mandrill_client.tags.all_time_series = MagicMock(return_value=[])
        self.stream.mandrill_client.webhooks.list = MagicMock(return_value=[])
        self.stream.metrics = metrics
        result_a = self.stream.read()
        result_b = self.stream.read()
        result_c = self.stream.read()

        self.assertEqual(result_a, [])
        self.assertEqual(result_b, [])
        self.assertEqual(result_c, None)

    def test_required_metric(self):
        metrics = [{ 
            "name":"senders",
            "path":"time_series",
            "required":"address",
            "category": "senders"
        }]
        res = [
            {"address": "a@a.a"},
            {"address": "b@b.b"}
        ]
        self.stream.metrics = metrics
        self.stream.mandrill_client.senders.list = MagicMock(return_value=res)
        self.stream.mandrill_client.senders.time_series = MagicMock()
        self.stream.read()

        # last call was the last address
        self.stream.mandrill_client.senders.time_series.assert_called_with(address="b@b.b")
        # called twice (one time for each address)
        self.assertEqual(self.stream.mandrill_client.senders.time_series.call_count, 2)

if __name__ == "__main__":
    unittest.main()
