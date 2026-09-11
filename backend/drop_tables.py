from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
try:
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("DROP TABLE IF EXISTS feedback;"))
        conn.execute(text("DROP TABLE IF EXISTS url_scans;"))
        conn.execute(text("DROP TABLE IF EXISTS message_scans;"))
        conn.execute(text("DROP TABLE IF EXISTS users;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        print("Dropped old tables successfully.")
except Exception as e:
    print(f"Error dropping tables: {e}")
