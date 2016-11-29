import panoply
import urllib2
import conf
import copy
import time
import json
from functools import partial
from itertools import chain
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

    @reportProgress
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
        return result   
    
    @staticmethod
    def reportProgress(fn):
        '''decorator for auto progress report'''
        def wrapper(*args):
            result = fn(*args)
            loaded = self.total - len(self.metrics)
            msg = "%s of %s metrics loaded" % (loaded, self.total)
            # args[0] is self
            args[0].progress(loaded, self.total, msg)
            return result
        return wrapper
    
    def getFn(self, metric, path=None):
        '''dynamically locate the right function to call from the sdk.'''
        return getattr(getattr(self.mandrill_client, metric['category']), path or metric['path'])
    
    def handleRequired(self, metric, required_field):
        '''for metrics that would need an extra api call before they can work.'''
        list_fn = self.getFn(metric, 'list')
        extracted_fields = [row.get(required_field) for row in list_fn() if row.get(required_field)]
        fn = self.getFn(metric)
        # for each field we have (for example each email we got from the list call)
        # do an api call on that field
        # for example mandrill_client.senders.time_series(address='someUnique@email.com')
        results = []
        for field in extracted_fields:
            # dynamically choose the paramater to send to the function
            param_dict = {'' + required_field: field}
            # the response from the api call contains an array, we need to add some info
            # on each of the result objects inside this array
            # the info is the param dict itself (for example adding address: 'blabla@a.a')
            result = [mergeDicts(param_dict, response_obj) for response_obj in fn(**param_dict)]
            results.append(result)
        # flatten the results (which are a list of lists) into flat list
        return list(chain.from_iterable(results))
    
    def handleRegular(self, metric):
        '''for your everyday metric.'''
        return self.getFn(metric)()

def mergeDicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z