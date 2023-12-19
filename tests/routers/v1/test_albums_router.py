from fastapi.testclient import TestClient
from app.main import app
from app.stores.sql_store import SqlStore
from app.dependency import get_store



client = TestClient(app)


def test_get_many_albums():
    response = client.get('/api/v1/albums?page=1&per_page=10')
    assert response.status_code == 200
    assert 'items' in response.json()
    assert 'count' in response.json()
