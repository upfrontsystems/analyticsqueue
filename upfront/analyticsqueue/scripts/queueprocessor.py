import sys
import logbook
from logbook import handlers

from redis import Redis
from redis.exceptions import ConnectionError

from rq import Queue, Worker
from rq.scripts.rqworker import format_colors, setup_loghandlers
from rq.scripts import add_standard_arguments
from rq.scripts import setup_redis


class RedisQueueArgs(object):
    """ Can be elaborated to read a config file.
    """
    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0

        self.burst = False
        self.name = 'Analytics queue processor'
        self.path = ''
        self.verbose = True
        self.queues = ['google_analytics_q',
                       'piwik_analytics_q']


def processqueue():
    args = RedisQueueArgs()
    setup_loghandlers(args)
    setup_redis(args)
    try:
        queues = map(Queue, args.queues)
        worker_name = Worker.redis_worker_namespace_prefix + args.name
        worker = Worker.find_by_key(worker_name)
        if worker:
            # get the stale worker to stop in order to start a new one
            print 'Stopping stale worker.'
            worker.register_death() 
        else:
            worker = Worker(queues, name=args.name)
        worker.work(burst=args.burst)
    except ConnectionError as e:
        print(e)
        sys.exit(1)
