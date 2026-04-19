import redis
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('REDIS_HOST')
port = os.getenv('REDIS_PORT')
username = os.getenv('REDIS_USERNAME')
password = os.getenv('REDIS_PASSWORD')
# "fake" implementation, true implementation out of scope for assignment

# create cells "database"
cells = {}
cells["45762"] = {"filename": "45762", "modality": "microscope", "type": "osteosarcoma", "species": "human"}
cells["46314"] = {"filename": "46314", "modality": "microscope", "type": "osteosarcoma", "species": "human"}
cells["1_512v"] = {"filename": "1_512v", "modality": "multiphoton", "type": "medium spiny neuron", "species": "mouse"}
cells["8_512v"] = {"filename": "8_512v", "modality": "confocal", "type": "protoplasmic astrocyte", "species": "rat"}
cells["8_512v"] = {"filename": "8_512v", "modality": "confocal", "type": "protoplasmic astrocyte", "species": "rat"}
cells["1132_512v"] = {"filename": "1132_512v", "modality": "confocal", "type": "cerebellar basket cell", "species": "rat"}


def main(host, port, password):
    try:
        client = redis.Redis(host=host, port=port, username=username, password=password, decode_responses=True)
        client.ping()
        print("inference connected to redis!")
    except redis.ConnectionError:
        print("inference redis connection issue :(")
        quit()

    # listen for image and file name
    subscriber = client.pubsub()
    subscriber.subscribe('new_image')
    print("Inference waiting for new images... (Press Ctrl+C to stop)")
    for message in subscriber.listen():
        if message['type'] == 'message':
            print(f"New Image Received: {message['data']}")
            filename = str(message['data'])
            # export inferences related to file
            client.publish('inferences', json.dumps(cells[filename]))
