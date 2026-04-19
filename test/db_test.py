import pytest
import fakeredis
import json
from db_service import db_entry, BIO_MAP

@pytest.fixture
def fake_client():
    return fakeredis.FakeRedis(decode_responses=True)

def test_biological_data_indexing(fake_client):
    # Test data based on your image table
    filename = "8_512v.jpg"
    data = {
        "filename": filename,
        "modality": "confocal",
        "type": "protoplasmic astrocyte",
        "species": "rat"
    }
    
    db_entry(fake_client, filename, data)
    
    # 1. Verify Hash storage
    stored_data = fake_client.hgetall(f"product:{filename}")
    assert stored_data["species"] == "rat"
    
    # 2. Verify ZSet Indexing
    expected_score = BIO_MAP["protoplasmic astrocyte"]
    actual_score = fake_client.zscore("idx:cell_types", filename)
    assert actual_score == expected_score

def test_search_by_cell_type(fake_client):
    # Seed data
    fake_client.zadd("idx:cell_types", {"45762.jpg": 1, "46314.jpg": 1, "1_512v.jpg": 2})
    
    # Simulate searching for 'osteosarcoma' (Score 1)
    results = fake_client.zrangebyscore("idx:cell_types", 1, 1)
    
    assert "45762.jpg" in results
    assert "46314.jpg" in results
    assert "1_512v.jpg" not in results