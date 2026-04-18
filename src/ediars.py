import redis
import threading


# please enter host

# please enter password

# keep those values
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# call inference, embedding, and db in separate threads, pass host and pw


# input loop
# publish new images
def broadcast(headline):
    # Publish the message to the 'new_image' channel
    r.publish('new_image', headline)
    print(f"📢 Broadcasted: {headline}")

broadcast("Redis Pub/Sub is surprisingly easy.")

# find images from DB
def search(headline):
    # Publish the message to the 'new_image' channel
    r.publish('search', headline)
    print(f"📢 Broadcasted: {headline}")

search(f"{user_query}")