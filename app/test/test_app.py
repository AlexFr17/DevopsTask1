import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import app

def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthySuper"

def test_index():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "version" in resp.get_json()
