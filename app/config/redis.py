import redis

# 1. Connect to the local Redis Docker container
# The default port for Redis is 6379
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    # 2. Test the connection
    if redis_client.ping():
        print("Successfully connected to Redis container!")
except redis.exceptions.ConnectionError:
    print("Could not connect to Redis. Is the container running?")
