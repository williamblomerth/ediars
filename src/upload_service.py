import redis
import pandas
import threading

# Connect to local Redis instance
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Create a pubsub object
subscriber = r.pubsub()

# Subscribe to a specific channel
subscriber.subscribe('new_image')

# print("Waiting for new images... (Press Ctrl+C to stop)")

# Listen for messages
for message in subscriber.listen():
    if message['type'] == 'message':
        print(f"New Image Received: {message['data']}")


def broadcast(headline):
    # Publish the message to the 'news_updates' channel
    r.publish('news_updates', headline)
    print(f"📢 Broadcasted: {headline}")

# Example usage
broadcast_news("Python 4.0 released (Just kidding!)")
broadcast_news("Redis Pub/Sub is surprisingly easy.")