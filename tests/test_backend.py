import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add backend directory to sys.path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')))

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings
from app.services.ml_service import ml_service

# For testing, we want to try connecting to the real DB as requested by user to verify MySQL.
# If it fails, the test will fail and we know DB is an issue.

client = TestClient(app)

def test_db_connection():
    engine = create_engine(settings.DATABASE_URL)
    try:
        connection = engine.connect()
        connection.close()
        assert True
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_ml_models_loading():
    ml_service.load_models()
    assert ml_service.url_model is not None, "URL Model failed to load"
    assert ml_service.message_model is not None, "Message Model failed to load"

def test_url_prediction():
    ml_service.load_models()
    res = ml_service.predict_url("http://secure-login-paypal.com/verify")
    assert "prediction" in res
    assert res["prediction"] in ["phishing", "legitimate"]
    assert "risk_score" in res

def test_message_prediction():
    ml_service.load_models()
    res = ml_service.predict_message("URGENT: Your account has been locked. Click here to verify.")
    assert "prediction" in res
    assert res["prediction"] in ["scam", "legitimate"]
    assert "risk_score" in res

def test_ml_generalization_diagnostic():
    ml_service.load_models()
    # Legitimate URLs that were previously misclassified
    legit1 = ml_service.predict_url("https://www.google.com")
    legit2 = ml_service.predict_url("https://www.microsoft.com")
    
    # Synthetic phishing URLs
    phish1 = ml_service.predict_url("http://paypal-login-security.example.com/verify-account")
    
    assert legit1["prediction"] == "legitimate", f"Google was classified as {legit1['prediction']}"
    assert legit2["prediction"] == "legitimate", f"Microsoft was classified as {legit2['prediction']}"
    
    # Due to feature extraction, phish1 should have a higher risk score or be classified as phishing
    # We at least ensure that the logic is evaluating it correctly.
    assert phish1["prediction"] == "phishing" or phish1["risk_score"] > 20, "Synthetic phishing failed to be flagged"

def test_auth_register_login():
    # Attempt to register a test user
    # Note: If user exists, it might fail. Let's use a random username.
    import uuid
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password = "password123"

    # Register
    res = client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    # If DB is down, this will fail. Let's allow 400 if user exists, but it's random so should be 200.
    if res.status_code == 500:
        pytest.fail(f"Register failed with 500: {res.text}")
    
    assert res.status_code == 200, f"Register failed: {res.text}"

    # Login
    res = client.post("/api/auth/login", data={
        "username": username,
        "password": password
    })
    assert res.status_code == 200, f"Login failed: {res.text}"
    token = res.json()["access_token"]

    # Test /me
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == username

    # Test Scan URL
    res = client.post("/api/scan/url", json={"url": "http://example.com"}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "prediction" in res.json()

    # Test Scan Message
    res = client.post("/api/scan/message", json={"message": "Hello world"}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "prediction" in res.json()

    # Test History
    res = client.get("/api/history/urls", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["total"] >= 1

    # Test Dashboard
    res = client.get("/api/dashboard/stats", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "url_scans" in res.json()

    # Test History Deletion
    # Bulk delete
    res = client.delete("/api/history/urls", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    # Verify it's empty
    res = client.get("/api/history/urls", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["total"] == 0

def test_auth_password_reset():
    # Attempt to request OTP for non-existent user should not fail (security)
    res = client.post("/api/auth/forgot-password", json={"email": "nobody@example.com"})
    assert res.status_code == 200
    assert "OTP has been sent" in res.json()["message"]
    
    # Attempt reset with invalid OTP
    res = client.post("/api/auth/reset-password", json={"email": "nobody@example.com", "otp": "000000", "new_password": "newpassword123"})
    assert res.status_code == 400
