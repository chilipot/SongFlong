import redis
from rq import Worker, Connection

conn = redis.from_url('redis://redis:6379')

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(['default'])
        worker.work()
