import os
import sys
import json
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.app.core.config import settings

def audit():
    print("=== PHASE 4: SUPABASE CONNECTION ===")
    supabase_url = settings.SUPABASE_DATABASE_URL
    if not supabase_url:
        print("FAIL: SUPABASE_DATABASE_URL is missing")
        return
    try:
        engine = create_engine(supabase_url)
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 1")).scalar()
            if res == 1:
                print("PASS: Supabase Connection Successful")
    except Exception as e:
        print(f"FAIL: Supabase connection failed: {e}")
        return

    print("\n=== PHASE 5: SUPABASE SCHEMA ===")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Found tables: {tables}")
    required_tables = ['app_users', 'app_url_scans', 'app_message_scans', 'app_feedback', 'app_password_resets']
    for req in required_tables:
        if req in tables:
            print(f"PASS: {req} exists.")
        else:
            print(f"FAIL: {req} missing.")

    print("\n=== PHASE 6: MYSQL VS SUPABASE DATA ===")
    expected_counts = {
        'app_users': 24,
        'app_url_scans': 15,
        'app_message_scans': 22,
        'app_feedback': 0,
        'app_password_resets': 0
    }
    with engine.connect() as conn:
        for t, exp in expected_counts.items():
            if t in tables:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
                diff = exp - count
                status = "PASS" if diff == 0 else "FAIL"
                print(f"{t}: Expected={exp}, Actual={count}, Diff={diff} -> {status}")

    print("\n=== PHASE 7: DATA INTEGRITY ===")
    with engine.connect() as conn:
        # Check orphaned url scans
        orphans = conn.execute(text("SELECT COUNT(*) FROM app_url_scans WHERE user_id NOT IN (SELECT id FROM app_users)")).scalar()
        print(f"Orphaned URL Scans: {orphans} -> {'PASS' if orphans == 0 else 'FAIL'}")
        
        # Check invalid roles
        invalid_roles = conn.execute(text("SELECT COUNT(*) FROM app_users WHERE role NOT IN ('USER', 'ADMIN')")).scalar()
        print(f"Invalid User Roles: {invalid_roles} -> {'PASS' if invalid_roles == 0 else 'FAIL'}")

        # Check risk score limits
        invalid_risk = conn.execute(text("SELECT COUNT(*) FROM app_url_scans WHERE risk_score < 0 OR risk_score > 100")).scalar()
        print(f"Invalid URL Risk Scores: {invalid_risk} -> {'PASS' if invalid_risk == 0 else 'FAIL'}")

    print("\n=== PHASE 11: ML VERIFICATION ===")
    try:
        from backend.app.services.ml_service import ml_service
        ml_service.load_models()
        if ml_service.url_model and ml_service.message_model:
            print("PASS: ML Models loaded successfully")
            url_res = ml_service.predict_url("http://secure-login-paypal.com/verify")
            print(f"Sample URL Prediction: {url_res['prediction']} (Risk: {url_res['risk_score']}) -> PASS")
            msg_res = ml_service.predict_message("URGENT: Click here to win a prize")
            print(f"Sample Message Prediction: {msg_res['prediction']} (Risk: {msg_res['risk_score']}) -> PASS")
        else:
            print("FAIL: Models failed to load")
    except Exception as e:
        print(f"FAIL: ML Verification failed: {e}")

if __name__ == "__main__":
    audit()
