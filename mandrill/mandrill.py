import panoply
import urllib2
import conf
import copy
import time
import json

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
BASE_URL = conf.BASE_URL
DAY_RANGE = conf.DAY_RANGE

class Mandrill(panoply.DataSource):

    def __init__(self, source, opt):
        super(Mandrill, self).__init__(source, opt)
        fromsec = int(time.time() - (DAY_RANGE * DAY))
        self._from = time.strftime("%Y-%m-%d", time.gmtime(fromsec))
        self._to = time.strftime("%Y-%m-%d", time.gmtime())
        self._metrics = copy.deepcopy( conf.metrics )
        self._total = len( self._metrics )
        self._key = source["key"]


    def read(self, n = None):
        if len(self._metrics) == 0:
            return None # No more data to consume
        metric = self._metrics[0]
        url = BASE_URL + metric["path"]
        body = {
            "key": self._key,
            "date_from": self._from,
            "date_to": self._to
        }
        # initiate the required item list for the given metric
        if "required" in metric and "requiredList" not in metric:
            metric["requiredList"] = self._getRequireds(metric)
            # if no required items were found continue to the next metric
            if not len( metric["requiredList"] ):
                self._metrics.pop(0)
                return self.read()


        requiredList = metric.get("requiredList", [])
        if len(requiredList) > 0:
            requiredName = metric["required"]
            requiredItem = requiredList[0]
            body[ requiredName ] = requiredItem

        result = self._request( url, body )
        # add the result type for each row
        for row in result:
            row["type"] = metric["name"]

        # if it wasn't the last required item just pop it from the metric
        # required list
        if len(requiredList) > 1 :
            metric["requiredList"].pop(0)

        # if it was the last required item or this metric don't have a required 
        # items pop the metric from the metric list
        else:
            self._metrics.pop(0)
            loaded = self._total - len(self._metrics)
            msg = "%s of %s metrics loaded" % (loaded, self._total)
            self.progress(loaded, self._total, msg)
        return result

    # get the required items for the given metrics and 
    # return the number for items found
    def _getRequireds(self, metric):
        url = BASE_URL + metric["listpath"]
        body = {
            "key": self._key
        }

        result = self._request(url, body)
        requiredName = metric["required"]
        return map(lambda row: row[requiredName], result)

    def _request(self, url, body):
        req = urllib2.Request(url)
        data = json.dumps( body )
        req.add_header("Content-Type", "application/json")

        self.log("POST", url)

        try:
            res = urllib2.urlopen(req, data)
        except urllib2.HTTPError, e:
            raise MandrillError.from_http_error(e)

        self.log("RESPONSE", url)

        return json.loads(res.read())


class MandrillError(Exception):

    # Transform the generic urllib2.HTTPError to more descriptive exception
    # based on the JSON error description provide by mandrill API
    @classmethod
    def from_http_error(cls, err):
        body = err.read()
        description = json.loads(body)
        if "message" in description:
            return cls(description["message"])
        return err
