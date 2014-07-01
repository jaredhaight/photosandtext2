from redis import Redis
from rq import Queue

low_queue = Queue('low', connection=Redis())
medium_queue = Queue('medium', connection=Redis())
high_queue = Queue('high', connection=Redis())
