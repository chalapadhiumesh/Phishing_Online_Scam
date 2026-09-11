from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
try:
    with engine.connect() as conn:
        res = conn.execute(text("DESCRIBE users"))
        for row in res:
            print(row)
except Exception as e:
    print(f"Error: {e}")
