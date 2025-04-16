from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.database import get_db_connection


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Test with mocked DB calls
def test_get_item_with_mocked_db(mocker):
    mock_db = mocker.patch('myapp.database.get_db', return_value=["mocked_item"])
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == ["mocked_item"]

