import hashlib
import datetime
import types

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
                  'previous_visit_time': {'processor': PreviousDateProcessor},
                  'current_visit_time':  {'processor': CurrentDateProcessor},
                  'visit_count':         {'processor': CountProcessor},
                 }

        for key in fields.keys():
            processor = fields[key].get('processor')
            
            value = history.get(key)
            value = value or getattr(self, key)
            value = processor.process(value, **history)
            setattr(self, key, value)
            history[key] = processor.serialize(value)

        connection.hmset(visitor_key, history)


    def _generate_unique_id(self):
        self.userid = self.settings.get('AUTHENTICATED_USER', 'Anonymous')
        seed = '%s%s%s' %(self.userid, self.user_agent, self.ip_address)
        self.unique_id = int(hashlib.md5(seed).hexdigest(), 16) & 0x7fffffff
        return self.unique_id


class DateProcessor(object):
    
    @classmethod
    def serialize(context, date):
        if isinstance(date, datetime.datetime):
            return date.isoformat()
        return date

    @classmethod
    def process(context, logged_date, **extra):
        if isinstance(logged_date, types.StringType):
            return datetime.datetime.strptime(
                logged_date, '%Y-%m-%dT%H:%M:%S.%f')
        return logged_date


class CurrentDateProcessor(DateProcessor):
    
    @classmethod
    def process(context, logged_date, **extra):
        now = datetime.datetime.utcnow()
        return now


class PreviousDateProcessor(DateProcessor):
    
    @classmethod
    def process(context, logged_date, **extra):
        prev_date = extra.get('previous_visit_date')
        if prev_date:
            return datetime.datetime.strptime(
                prev_date, '%Y-%m-%dT%H:%M:%S.%f')
        return datetime.datetime.utcnow()


class CountProcessor(object):
    
    @classmethod
    def serialize(context, counter):
        return counter
    
    @classmethod
    def process(context, historical_counter, **extra):
        return int(historical_counter) +0 
