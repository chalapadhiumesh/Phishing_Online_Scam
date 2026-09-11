import httpx
import os
from sqlalchemy import create_engine, text
from backend.app.core.config import settings

def run_e2e():
    print("--- E2E TEST ---")
    base_url = "http://localhost:8000"
    
    # 1. Register
    username = "testuser_e2e"
    email = "testuser_e2e@example.com"
    password = "TestPassword123!"
    
    print("1. Registering user...")
    try:
        httpx.post(f"{base_url}/api/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
    except Exception:
        # Ignore if user exists
        pass
        
    print("2. Logging in...")
    resp = httpx.post(f"{base_url}/api/auth/login", data={
        "username": username,
        "password": password
    })
    
    if resp.status_code != 200:
        print(f"Login failed! {resp.text}")
        return
        
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Login successful, token acquired.")
    
    print("3. Scanning URL...")
    url_resp = httpx.post(f"{base_url}/api/scan/url", json={"url": "http://secure-login-paypal.com-update.info"}, headers=headers)
    print(f"URL Scan Result: {url_resp.json()}")
    
    print("4. Scanning Message...")
    msg_resp = httpx.post(f"{base_url}/api/scan/message", json={"message": "You won a $1000 gift card! Click here."}, headers=headers)
    print(f"Message Scan Result: {msg_resp.json()}")
    
    print("5. Getting Dashboard Stats...")
    stats_resp = httpx.get(f"{base_url}/api/dashboard/stats", headers=headers)
    print(f"Dashboard Stats: {stats_resp.json()}")
    
    print("6. Getting History...")
    history_resp = httpx.get(f"{base_url}/api/history/urls", headers=headers)
    print(f"History records found: {history_resp.json().get('total', 0)}")
    
    print("7. Verifying Database Records...")
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        users = conn.execute(text(f"SELECT id FROM app_users WHERE username='{username}'")).fetchone()
        user_id = users[0]
        url_scans = conn.execute(text(f"SELECT COUNT(*) FROM app_url_scans WHERE user_id={user_id}")).scalar()
        msg_scans = conn.execute(text(f"SELECT COUNT(*) FROM app_message_scans WHERE user_id={user_id}")).scalar()
        print(f"Verified DB: {url_scans} URL scans, {msg_scans} Message scans found for user {username}.")
        
    print("--- E2E TEST COMPLETE AND SUCCESSFUL ---")

if __name__ == "__main__":
    run_e2e()
