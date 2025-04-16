import pytest
from fastapi.testclient import TestClient

# Attempt to import the FastAPI app
try:
    from backend.app.main import app
    client = TestClient(app)  # Initialize the TestClient with the app if imported successfully
except ModuleNotFoundError as e:
    print(f"⚠️ WARNING: Failed to import app: {e}")
    app = None
    client = None  # Ensure client is not initialized if the app is missing

# Define your fixture for signup data
@pytest.fixture
def signup_data():
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!"
    }

# Check if the client is initialized before running the tests
@pytest.mark.skipif(client is None, reason="App not imported correctly")
def test_signup_success(mocker, signup_data):
    # Mock dependencies
    mocker.patch("backend.app.services.signup.store_user_in_database", return_value=True)
    mocker.patch("backend.app.utils.password_checks.validate_password", return_value=(True, "Valid"))
    mocker.patch("backend.app.utils.password_checks.hash_password", return_value="hashed_password")
    mocker.patch("backend.app.utils.token_generation.create_access_token", return_value="access_token")
    mocker.patch("backend.app.utils.token_generation.create_refresh_token", return_value="refresh_token")

    response = client.post("/signup", json=signup_data)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User signed up successfully"
    assert data["success"] is True
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.skipif(client is None, reason="App not imported correctly")
def test_signup_password_mismatch(signup_data):
    signup_data["confirm_password"] = "Different123"
    response = client.post("/signup", json=signup_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Passwords do not match"


@pytest.mark.skipif(client is None, reason="App not imported correctly")
def test_signup_invalid_password(mocker, signup_data):
    mocker.patch("backend.app.utils.password_checks.validate_password", return_value=(False, "Too weak"))

    response = client.post("/signup", json=signup_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Too weak"


@pytest.mark.skipif(client is None, reason="App not imported correctly")
def test_login_success(mocker):
    login_data = {"email": "test@example.com", "password": "StrongPass123!"}

    # Mock verify_login and token creation
    mocker.patch("backend.app.services.login.verify_login", return_value=True)
    mocker.patch("backend.app.utils.token_generation.create_access_token", return_value="access_token")
    mocker.patch("backend.app.utils.token_generation.create_refresh_token", return_value="refresh_token")

    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["success"] is True
    assert data["access_token"] == "access_token"
    assert data["refresh_token"] == "refresh_token"
    assert data["Welsby"] == "TWat"


@pytest.mark.skipif(client is None, reason="App not imported correctly")
def test_login_invalid_credentials(mocker):
    login_data = {"email": "test@example.com", "password": "WrongPass!"}
    mocker.patch("backend.app.services.login.verify_login", return_value=False)

    response = client.post("/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
