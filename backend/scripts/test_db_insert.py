import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.core.database import SessionLocal
from backend.app.models.user import User
import uuid

def test_insert():
    db = SessionLocal()
    try:
        username = f"debuguser_{uuid.uuid4().hex[:8]}"
        email = f"{username}@example.com"
        
        new_user = User(
            username=username,
            email=email,
            password_hash="testhash"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("Success! Inserted:", new_user.id)
    except Exception as e:
        print("Error during insert:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_insert()
