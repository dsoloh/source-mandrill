import unittest
import urllib2
import json

from io import BytesIO
from mock import MagicMock
from panoply_mandrill import PanoplyMandrill, metrics as real_metrics

BASE_URL = "https://mandrillapp.com/api/1.0/"

OPTIONS = {
    "logger": lambda *args: None # don't log on test 
}

class TestMandrill(unittest.TestCase):

    def setUp(self):
        self.orig_metrics = real_metrics
        self.orig_urlopen = urllib2.urlopen

    def tearDown(self):
        real_metrics = self.orig_metrics
        urllib2.urlopen = self.orig_urlopen

    def test_defaults(self):
        source = {"key":"MandrillKey"}
        PanoplyMandrill(source, OPTIONS)
        self.assertEqual(source["idpattern"], IDPATTERN)
        self.assertEqual(source["destination"], DESTINATION)

    def test_simple_request(self):
        real_metrics = [{ 
            "name":"metric",
            "path": "metric.json"
        }]
        res = BytesIO("[]")
        urllib2.urlopen = MagicMock(return_value=res)
        
        PanoplyMandrill({
            "key":"MandrillKey"
        }, OPTIONS).read()
        
        req, body = urllib2.urlopen.call_args[0]
        body = json.loads(body)
        url = BASE_URL + "metric.json"
        
        self.assertEqual(req.get_full_url(), url)
        self.assertEqual(body.get("key"), "MandrillKey")

    def test_result(self):
        real_metrics = [{
            "name":"metric",
            "path":"metric.json"
        }]

        urlRes = BytesIO(json.dumps([{"hello":"world"}]))
        urllib2.urlopen = MagicMock(return_value=urlRes)
        
        stream = PanoplyMandrill({
            "key":"MandrillKey"
        }, OPTIONS)
        result = stream.read()[0]
        self.assertEqual(result.get("type"), "metric")
        self.assertEqual(result.get("hello"), "world")

    def test_iterate_metrics(self):
        real_metrics = [
            {
                "name":"metric1",
                "path":"metric1.json"
            },
            {
                "name":"metric2",
                "path":"metric2.json"
            }

        ]
        res1, res2 = BytesIO("[]"), BytesIO("[]")
        urllib2.urlopen = MagicMock(side_effect=[res1, res2])

        stream = PanoplyMandrill({
            "key":"MandrillKey"
        }, OPTIONS)
        stream.read()
        stream.read()
        self.assertEqual(urllib2.urlopen.call_count, 2)

        # make sure we done
        isNone = stream.read()
        self.assertEqual(isNone, None)

    def test_error(self):
        real_metrics = [{
            "name":"metric",
            "path":"metric.json"
        }]
        res = BytesIO(json.dumps({
            "status":"error",
            "code": -1,
            "name":"invalid_key",
            "message":"invalid API key"
        }))

        e = urllib2.HTTPError("url", 500, "Server Error", {}, res)
        urllib2.urlopen = MagicMock(side_effect=e)
        stream = PanoplyMandrill({
            "key":"invalid"
        }, OPTIONS )

        try:
            stream.read()
        except MandrillError, e:
            self.assertEqual(str(e), "invalid API key")

    def test_required_metric(self):
        real_metrics = [{
            "name":"metric",
            "path":"metric.json",
            "required":"name",
            "listpath":"metric/list.json"
        }]

        res1 = BytesIO(json.dumps([
            {"name":"id1"},
            {"name":"id2"}
        ]))
        res2 = BytesIO("[{}]")
        res3 = BytesIO("[{}]")

        mock = MagicMock();
        mock.side_effect = [res1, res2, res3]
        urllib2.urlopen = mock

        stream = PanoplyMandrill({
            "key":"MandrillKey"
        }, OPTIONS)
        result = stream.read()[0]

        args = urllib2.urlopen.call_args_list
        self.assertEqual(mock.call_count, 2)
        req1, body1 = args[0][0]
        req2, body2 = args[1][0]
        body1 = json.loads(body1)
        body2 = json.loads(body2)
        url1 = BASE_URL + "metric/list.json"
        url2 = BASE_URL + "metric.json"
        self.assertEqual(req1.get_full_url(), url1)
        self.assertEqual(req2.get_full_url(), url2)
        self.assertEqual(body2.get("name"), "id1")
        self.assertEqual(result.get("name"), "id1") # add the name to the result
        
        # iterate over the required list
        result = stream.read()[0]
        self.assertEqual(mock.call_count, 3)
        req3, body3 = args[2][0]
        body3 = json.loads(body3)
        self.assertEqual(body3.get("name"), "id2")
        self.assertEqual(result.get("name"), "id2") # add the name to the result

        # make sure we done
        isNone = stream.read()
        self.assertEqual(isNone, None)

if __name__ == "__main__":
    unittest.main()
