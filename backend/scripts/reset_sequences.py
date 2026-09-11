import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, text
from backend.app.core.config import settings

def reset_sequences():
    print("Resetting PostgreSQL sequences...")
    engine = create_engine(settings.SUPABASE_DATABASE_URL)
    
    tables = [
        "app_users",
        "app_url_scans",
        "app_message_scans",
        "app_password_resets",
        "app_feedback"
    ]
    
    with engine.begin() as conn:
        for table in tables:
            seq_name = f"{table}_id_seq"
            try:
                # Check if there are any rows to avoid resetting to NULL
                res = conn.execute(text(f"SELECT MAX(id) FROM {table}"))
                max_id = res.scalar()
                
                if max_id:
                    conn.execute(text(f"SELECT setval('{seq_name}', {max_id})"))
                    print(f"Sequence {seq_name} reset to {max_id}")
                else:
                    print(f"Sequence {seq_name} left at default (table empty)")
            except Exception as e:
                print(f"Failed to reset {seq_name}: {e}")

if __name__ == "__main__":
    reset_sequences()
