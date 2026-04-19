import redis
import sys
import os
import json
import vtracer
# "fake" implementation, true implementation out of scope for assignment


def main(host, port, password):
    # take in host and pw, connect to redis
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..')))
    # host = sys.argv[1]
    # port = sys.argv[2]
    # password = sys.argv[3]
    try:
        client = redis.Redis(host=host, port=port, password=password, decode_responses=True)
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
