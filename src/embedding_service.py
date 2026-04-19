import redis
import sys
import os
import json
import vtracer
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('REDIS_HOST')
port = os.getenv('REDIS_PORT')
username = os.getenv('REDIS_USERNAME')
password = os.getenv('REDIS_PASSWORD')
# "fake" implementation, true implementation out of scope for assignment


def main(host, port, password):
    try:
        client = redis.Redis(host=host, port=port, username=username, password=password, decode_responses=True)
        client.ping()
        print("embedding connected to redis!")
    except redis.ConnectionError:
        print("embedding redis connection issue :(")
        quit()

    # listen for inferences
    subscriber = client.pubsub()
    subscriber.subscribe('inferences')
    print("embedding waiting for inferences... (Press Ctrl+C to stop)")
    for message in subscriber.listen():
        if message['type'] == 'message':
            print(f"Inference Received: {message['data']}")
            objects = json.loads(message['data'])
            vtracer.convert_image_to_svg(input_path, output_path)
            objects["image_vec"] = output_path
            # publish image_data
            client.publish('image_data', json.dumps(objects))
