import redis
import os
import sys
import threading
from pathvalidate import is_valid_filepath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..')))
import src.inference_service as inference_service
import src.embedding_service as embedding_service
import src.db_service as db_service


def broadcast(client, headline):
    # Publish the message to the 'new_image' channel
    client.publish('new_image', headline)
    print(f"📢 broadcasted: {headline}")


def search(client, headline):
    # Publish the message to the 'new_image' channel
    client.publish('search', headline)
    print(f"📢 searched: {headline}")


def preprocess_input(raw_text):
    # Clean the user input (lowercase, strip whitespace).
    return raw_text.strip().lower()


def listening(client):
    # listen while still processing user input
    subscriber = client.pubsub()
    subscriber.subscribe('results', 'status')
    print("ediars waiting for results... (Press Ctrl+C to stop)")
    for message in subscriber.listen():
        if message['type'] == 'message':
            channel = message['channel']
            if channel == 'results':
                print(f"search result(s): {message['data']}")
            elif channel == 'status':
                print(f"status update: {message['data']}")


def main():
    print("--- [ welcome to ediars ] ---\n")

    # get host
    host = input("please enter host: ")
    host = str(host)

    # get port
    port = input("please enter port: ")
    port = int(port)

    # get username
    username = input("please enter username: ")
    username = str(username)

    # get password
    password = input("please enter password: ")
    password = str(password)

    # connect to redis
    try:
        client = redis.Redis(host=host, port=port, username=username, password=password, decode_responses=True)
        client.ping()
        print("connected to redis!")
    except redis.ConnectionError as e:
        print(f"redis connection issue : {e}")
        quit()

    # start submodule threads
    try:
        threads = []
        inference = threading.Thread(target=inference_service.main, args=(host,port,password,))
        embedding = threading.Thread(target=embedding_service.main, args=(host,port,password,))
        db = threading.Thread(target=db_service.main, args=(host,port,password,))
        listen = threading.Thread(target=listening, args=(client,))
        threads.append(inference, embedding, db, listen)
    except:
        print("system error, try again :(")
        quit()

    while True:

        user_input = input("please provide a new file path for upload, or search a keyword: ")

        try:
            # if user provided a filepath
            if is_valid_filepath(user_input.strip(), platform="Windows"):
                if os.path.isfile(user_input.strip()):
                    filename = os.path.basename(user_input.strip())
                    broadcast(client, filename)
                    print(f"ediars: image processing in progress.")
                    continue
                else:
                    print("ediars: sorry, that file does not exist.")
                    continue

            # if user is searching for a keyword
            else:
                clean_input = preprocess_input(user_input)
                if clean_input == "exit":
                    print("\n\nediars: goodbye!")
                    break
                elif clean_input == "quit":
                    print("\n\nediars: see you next time!")
                    break
                else:
                    search(client, clean_input)
                    print(f"ediars: searching for {clean_input}")

            # listen for responses

        except KeyboardInterrupt:
            print("\n\nediars: detected ctrl+c. powering down... goodbye!")
            sys.exit()


if __name__ == "__main__":
    main()