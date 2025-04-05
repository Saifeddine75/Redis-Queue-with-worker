
import json
from random import random

import redis

from app import config



def redis_db():
    """Initialize Redis connection."""
    db = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db,
        password=config.redis_password,
        decode_responses=True,
    )
    # Verify connection
    try:
        db.ping()
        print("Connected to Redis")
    except redis.ConnectionError:
        print("Failed to connect to Redis")
        return None

    return db

def redis_queue_push(db, message):
    """Push data to Redis queue."""
    try:
        db.lpush(config.redis_queue_name, message)
        print(f"Data pushed to {config.redis_queue_name}: {message}")
    except redis.RedisError as e:
        print(f"Failed to push data to Redis: {e}")


def redis_queue_pop(db):
    """Pop data from Redis queue."""
    try:
        _, message_json = db.brpop(config.redis_queue_name)
        print(f"Data popped from {config.redis_queue_name}: {message_json}")
        return message_json
    except redis.RedisError as e:
        print(f"Failed to pop data from Redis: {e}")
        return None
    

def process_message(db, message_json):
    message = json.loads(message_json)
    print(f"Message received: id={message['data']['message_number']}")

    # Simulate processing errors
    processed_success = random.choices([True, False], weights=[5, 1], k=1)[0]

    if processed_success:
        print(f"Message {message['data']['message_number']} processed successfully.")
    else:
        print(f"Message {message['data']['message_number']} failed to process.")
        # Push the message back to the queue for retry
        redis_queue_push(db, message_json)


def main():
    """Consumes messages from the Redis queue."""
    db = redis_db()
    if not db:
        return

    while True:
        message_json = redis_queue_pop(db)
        if message_json:
            process_message(db, message_json)
        else:
            print("No messages in the queue. Waiting...")
            break

    # Pop the message from the queue
    redis_queue_pop(db)