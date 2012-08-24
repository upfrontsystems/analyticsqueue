from redis import Redis
from rq import Queue


    def __init__(self, 
                 ):
def get_q(host='localhost', port=6379,
          db=0, password=None, socket_timeout=None,
          connection_pool=None, charset='utf-8',
          errors='strict', decode_responses=False,
          unix_socket_path=None, q_name):

    connection = Redis()
    q = Queue(name=q_name, connection=connection)
    return q
