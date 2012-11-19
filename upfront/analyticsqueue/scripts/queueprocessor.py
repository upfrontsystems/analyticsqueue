import logbook, argparse, sys
from logbook import handlers

from redis import Redis
from redis.exceptions import ConnectionError

from rq import Queue, Worker
from rq.worker import red
from rq.scripts.rqworker import format_colors
from rq.scripts import setup_redis


class AnalyticsQueueConfig(argparse.ArgumentParser):
    """ Can be elaborated to read a config file.
    """
    def __init__(self):
        description='A Redis queue processor.'
        super(AnalyticsQueueConfig, self).__init__(description=description)
        self.setup_args()
        self.parse_args()
        self.setup_loghandlers()
    
    def parse_args(self):
        args = super(AnalyticsQueueConfig, self).parse_args()
        for name, value in args._get_kwargs():
            setattr(self, name, value)

    def setup_args(self):
        self.add_argument('--host',
                           '-H',
                           default='localhost',
                           help='The Redis hostname (default: localhost)')

        self.add_argument('--port',
                           '-p',
                           type=int,
                           default=6379,
                           help='The Redis portnumber (default: 6379)')

        self.add_argument('--db',
                           '-d',
                           type=int,
                           default=0,
                           help='The Redis database (default: 0)')

        self.add_argument('--burst',
                           '-b',
                           action='store_true',
                           default=False,
                           help='Run in burst mode (quit after all work is done)')

        self.add_argument('--name',
                           '-n',
                           default='Upfront analytics queue processor',
                           help='Specify a different name')

        self.add_argument('--path',
                           '-P',
                           default='.',
                           help='Specify the import path.')

        self.add_argument('--verbose',
                           '-v',
                           action='store_true',
                           default=False,
                           help='Show more output')

        self.add_argument('queues',
                          nargs='*',
                          default = ['google_analytics_q',
                                     'piwik_analytics_q'],
                          help='The queues to listen on (default: \'default\')')

    def setup_loghandlers(self):
        if self.verbose:
            self.loglevel = logbook.DEBUG
            self.formatter = None
        else:
            self.loglevel = logbook.INFO
            self.formatter = format_colors

        handlers.NullHandler(bubble=False).push_application()

        handler = handlers.StreamHandler(sys.stdout,
                                         level=self.loglevel,
                                         bubble=False)
        if self.formatter:
            handler.formatter = self.formatter
        handler.push_application()

        handler = handlers.StderrHandler(level=logbook.WARNING,
                                         bubble=False)
        if self.formatter:
            handler.formatter = self.formatter
        handler.push_application()

def processqueue():
    config = AnalyticsQueueConfig()
    if config.path:
        sys.path = config.path.split(':') + sys.path

    setup_redis(config)
    try:
        queues = map(Queue, config.queues)
        worker_name = Worker.redis_worker_namespace_prefix + config.name
        worker = Worker.find_by_key(worker_name)
        if worker:
            # get the stale worker to stop in order to start a new one
            worker.log.info(red('Stopping stale worker %s' % (worker.name,)))
            worker.register_death()

        worker = Worker(queues, name=config.name)
        worker.work(burst=config.burst)
    except ConnectionError as e:
        print(e)
        sys.exit(1)
