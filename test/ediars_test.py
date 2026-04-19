import pytest
import fakeredis
from unittest.mock import patch
from ediars import preprocess_input, broadcast, search

@pytest.fixture
def fake_client():
    return fakeredis.FakeRedis(decode_responses=True)

def test_preprocess_input():
    assert preprocess_input("  FILE_Name.JPG  ") == "file_name.jpg"
    assert preprocess_input("SearchTerm") == "searchterm"

def test_broadcast_publishes_message(fake_client):
    pubsub = fake_client.pubsub()
    pubsub.subscribe('new_image')
    
    filename = "test_image.png"
    broadcast(fake_client, filename)
    
    # Check if message was received on the channel
    message = pubsub.get_message(ignore_subscribe_messages=True)
    assert message['channel'] == 'new_image'
    assert message['data'] == filename

def test_search_publishes_message(fake_client):
    pubsub = fake_client.pubsub()
    pubsub.subscribe('search')
    
    query = "gadget"
    search(fake_client, query)
    
    message = pubsub.get_message(ignore_subscribe_messages=True)
    assert message['channel'] == 'search'
    assert message['data'] == query