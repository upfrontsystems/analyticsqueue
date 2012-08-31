import hashlib
import datetime

from redis import Redis
from pyga.entities import Visitor as BaseVisitor

ROOT_NAME = 'visitor'


class Visitor(BaseVisitor):

    def __init__(self, settings):
        self.settings = settings
        super(Visitor, self).__init__()  
        self.extract_from_server_meta(self.settings)
        self._generate_unique_id()

        connection = Redis(port=settings['redis-port'])

        # get the historical data from redis
        visitor_key = '%s%s' %(ROOT_NAME, self.unique_id)
        history = connection.hgetall(visitor_key)
        
        fields = {'first_visit_time':    {'processor': DateProcessor},
                  'previous_visit_time': {'processor': DateProcessor},
                  'current_visit_time':  {'processor': CurrentDateProcessor},
                  'visit_count':         {'processor': CountProcessor},
                 }

        for key in fields.keys():
            processor = fields[key].get('processor')
            
            value = history.get(key)
            value = value or getattr(self, key)
            value = processor.process(value, history)
            setattr(self, key, value)
            history[key] = value

        connection.hmset(visitor_key, history)


    def _generate_unique_id(self):
        self.userid = self.settings.get('AUTHENTICATED_USER', 'Anonymous')
        if self.userid != 'Anonymous':
            self.unique_id = int(hashlib.md5(self.userid).hexdigest(), 16)
        else: 
            self.unique_id = int(hashlib.md5(self.ip_address).hexdigest(), 16)
        return self.unique_id


class DateProcessor(object):
    
    @classmethod
    def process(context, historical_date, **extra):
        return historical_date


class CurrentDateProcessor(object):
    
    @classmethod
    def process(context, historical_date, **extra):
        now = datetime.utcnow()
        return now


class CountProcessor(object):
    
    @classmethod
    def process(context, historical_counter, **extra):
        return int(historical_counter) +1 
