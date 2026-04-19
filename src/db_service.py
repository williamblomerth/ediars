import redis
import sys
import os
import json


def db_entry(client, filename, data):
    # unique identifier
    key = f"product:{filename}"

    # check if exists before adding
    if client.exists(key):
        print(f"error: {filename} already exists!")
        return False

    # create payload
    # use hash to store multiple attributes in one place
    data = {
        "name": name,
        "price": price,
        "stock": stock,
        "last_updated": "2026-04-19"
    }

    # add to db
    client.hset(key, mapping=data)
    client.zadd("idx:product_price", {"laptop_001": 1999})

    print(f"successfully added {filename} to database.")


def main(host, port, password):
    # take in host and pw, connect to redis
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..')))
    host = sys.argv[1]
    port = sys.argv[2]
    password = sys.argv[3]
    try:
        client = redis.Redis(host=host, port=port, password=password, decode_responses=True)
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
                results = client.zrangebyscore("idx:type", message['data'])
                client.publish('results', results)
