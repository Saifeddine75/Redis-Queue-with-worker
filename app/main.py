
import random
from datetime import datetime
from json import dumps
from time import sleep
from uuid import uuid4

import redis

import config



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


def main(num_messages: int, delay: float = 1):
    """Main function to push messages to Redis queue."""
    db = redis_db()
    if not db:
        return

    for i in range(num_messages):
        message = {
            "id": str(uuid4()),
            "timestamp": datetime.now().isoformat(),
            "data": {
                "message_number": i,
                "x": random.randrange(0, 100),
                "y": random.randrange(0, 100),
            }
        }

        message_json = dumps(message)

        print(f"Sending message {i+1} (id={message['id']})")
        redis_queue_push(db, message_json)

        sleep(delay)


if __name__ == "__main__":
    # Example usage: push 10 messages with a delay of 2 seconds between each
    main(num_messages=10, delay=0.1)