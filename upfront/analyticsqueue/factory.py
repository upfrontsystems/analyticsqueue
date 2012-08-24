from redis import Redis
from rq import Queue


def get_q(q_name, host='localhost', port=6379,
          db=0, password=None, socket_timeout=None,
          connection_pool=None, charset='utf-8',
          errors='strict', decode_responses=False,
          unix_socket_path=None):

    connection = Redis(port=port)
    q = Queue(name=q_name, connection=connection)
    return q
