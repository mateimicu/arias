from rq import Queue
from redis import Redis
from job import a, run

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
j = q.enqueue(a.run)
j1 = q.enqueue(a.run)
j2 = q.enqueue(a.run)
