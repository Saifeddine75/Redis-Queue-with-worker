import os

redis_host = "localhost"
redis_port = 6379
redis_db = 0
redis_password = os.getenv("REDIS_PASSWORD")
redis_queue_name = "queue-1"