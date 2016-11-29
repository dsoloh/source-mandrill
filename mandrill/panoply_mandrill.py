import panoply
import urllib2
import conf
import copy
import time
import json
from functools import partial
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

        source["destination"] = source.get("destination") or DESTINATION
        source["idpattern"] = source.get("idpattern") or IDPATTERN

        fromsec = int(time.time() - (DAY_RANGE * DAY))
        self.fromTime = time.strftime("%Y-%m-%d", time.gmtime(fromsec))
        self.toTime = time.strftime("%Y-%m-%d", time.gmtime())
        self.metrics = copy.deepcopy(conf.metrics)
        self.total = len(self.metrics)
        self.key = source.get('key')
        self.mandrill_client = Mandrill(self.key)
        # TODO: handle the error raised with wrong api key
        self.mandrill_client.users.ping()

    def read(self, n = None):
        if len(self.metrics) == 0:
            return None # No more data to consume
        metric = self.metrics[0]

        # choose the right handler for this metric
        required_field = metric.get("required")
        handler = partial(self.handleRequired, metric, required_field) if required_field \
                    else partial(self.handleRegular, metric)

        result = handler()
        # add type and key to each row
        result = [dict(type=metric["name"], key=self.key, **row) for row in result]
        self.metrics.pop(0)
        self.reportProgress()
        return result
    
    def reportProgress(self):
        loaded = self.total - len(self.metrics)
        msg = "%s of %s metrics loaded" % (loaded, self.total)
        self.progress(loaded, self.total, msg)
    
    def getFn(self, metric, path=None):
        # dynamically locate the right function to call from the sdk.
        return getattr(getattr(self.mandrill_client, metric['category']), path or metric['path'])
    
    def handleRequired(self, metric, required_field):
        # for metrics that would need an extra api call before they can work
        list_fn = self.getFn(metric, 'list')
        extracted_fields = [row.get(required_field) for row in list_fn() if row.get(required_field)]
        fn = self.getFn(metric)
        # dynamically choose the paramater to send to the function
        return [fn(**{'' + required_field: field} for field in extracted_fields)]
    
    def handleRegular(self, metric):
        # for your everyday metric
        return self.getFn(metric)()
