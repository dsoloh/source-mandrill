import panoply
import urllib2
import conf
import copy
import time
import json
from mandrill import Mandrill, InvalidKeyError

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
BASE_URL = conf.BASE_URL
DAY_RANGE = conf.DAY_RANGE
DESTINATION = "mandrill_{type}"
IDPATTERN = "{time}-{key}-{type}-{name}-{address}-{url}"

class PanoplyMandrill(panoply.DataSource):

    def __init__(self, source, opt):
        super(PanoplyMandrill, self).__init__(source, opt)

        if "destination" not in source:
            source["destination"] = DESTINATION

        if "idpattern" not in source:
            source["idpattern"] = IDPATTERN

        fromsec = int(time.time() - (DAY_RANGE * DAY))
        self.fromTime = time.strftime("%Y-%m-%d", time.gmtime(fromsec))
        self.toTime = time.strftime("%Y-%m-%d", time.gmtime())
        self.metrics = copy.deepcopy(conf.metrics)
        self.total = len(self.metrics)
        self.mandrill_client = mandrill.Mandrill(source.get('key'))
        try:
            self.mandrill_client.users.ping()
        except InvalidKeyError:
            raise Error('WOWOWOWOWOWOWOWOWOWOWO')

    def read(self, n = None):
        return None
        if len(self.metrics) == 0:
            return None # No more data to consume
        metric = self.metrics[0]
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
            if not len(metric["requiredList"]):
                self.metrics.pop(0)
                return self.read()


        requiredList = metric.get("requiredList", [])
        additionalData = {}
        if len(requiredList):
            requiredName = metric["required"]
            requiredItem = requiredList[0]
            additionalData[requiredName] = requiredItem

        body.update(additionalData)
        result = self._request(url, body)
        # add the result type for each row
        for row in result:
            row["type"] = metric["name"]
            row["key"] = self._key
            row.update(additionalData)

        # if it wasn't the last required item just pop it from the metric
        # required list
        if len(requiredList):
            metric["requiredList"].pop(0)

        # if it was the last required item or this metric don't have a required 
        # items pop the metric from the metric list
        if not len(requiredList):
            self.metrics.pop(0)
            loaded = self._total - len(self.metrics)
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
        return [row.get(requiredName) for row in result]
