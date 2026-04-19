import pytest
import fakeredis
import json
from db_service import db_entry

@pytest.fixture
def fake_client():
    # Setup a clean fake redis instance for every test
    return fakeredis.FakeRedis(decode_responses=True)

def test_db_entry_new_product(fake_client):
    filename = "test_image.jpg"
    data = {"type": "electronics", "description": "a cool gadget"}
    
    # Run the function
    db_entry(fake_client, filename, data)
    
    # Assert Hash exists
    assert fake_client.exists(f"product:{filename}")
    assert fake_client.hgetall(f"product:{filename}") == data
    
    # Assert ZSet index exists (Note: data["type"] is used as a member in your code)
    # Note: In your script, you use zadd with a dict. Fakeredis handles this.
    zset_key = f"idx:{filename}"
    assert fake_client.exists(zset_key)

def test_db_entry_duplicate_product(fake_client, capsys):
    filename = "duplicate.jpg"
    data = {"type": "test"}
    
    # Add it once
    db_entry(fake_client, filename, data)
    
    # Try adding again
    result = db_entry(fake_client, filename, data)
    
    # Assertions
    assert result is False
    captured = capsys.readouterr()
    assert f"error: {filename} already exists!" in captured.out