import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Test the connection
try:
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Redis isn't running.")

# listen for vector and objects, add them to DB


# listen for queries, return images matching queries