from redis import Redis
from rq import Queue


def get_q(q_name):
    connection = Redis()
    q = Queue(name=q_name, connection=connection)
    return q
