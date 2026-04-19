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

BIO_MAP = {
    "osteosarcoma": 1,
    "medium spiny neuron": 2,
    "protoplasmic astrocyte": 3,
    "cerebellar basket cell": 4
}


def db_entry(client, filename, data):
    # unique identifier
    key = f"product:{filename}"

    # check if exists before adding
    if client.exists(key):
        print(f"error: {filename} already exists!")
        return False

    # add to db
    client.hset(key, mapping=data)
    cell_type = data.get("type", "").lower()
    score = BIO_MAP.get(cell_type, 0)
    client.zadd("idx:cell_types", {filename: score})

    print(f"successfully added {filename} to database.")


def main(host, port, password):

    try:
        client = redis.Redis(host=host, port=port, username=username, password=password, decode_responses=True)
        client.ping()
        print("db connected to redis!")
    except redis.ConnectionError:
        print("db redis connection issue :(")
        quit()

    # listen for image_data and searches
    subscriber = client.pubsub()
    subscriber.subscribe('image_data', 'search')
    print("db is listening... (Press Ctrl+C to stop)")
    for message in subscriber.listen():
        if message['type'] == 'message':
            channel = message['channel']
            if channel == 'image_data':
                print(f"embedding received: {message['data']}")
                tmp = json.loads(message['data'])
                filename = tmp["filename"]
                data = tmp
                # add to db
                db_entry(client, filename, data)
            elif channel == 'search':
                print(f"search received: {message['data']}")
                # search db for filenames with objects matching search
                results = client.zrangebyscore("filename:type", message['data'])
                client.publish('results', results)
