import os
import sys
import json
from sqlalchemy import create_engine, MetaData, Table

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.app.core.config import settings

backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "migration", "mysql_backup")
os.makedirs(backup_dir, exist_ok=True)

def backup_mysql():
    engine = create_engine(settings.DATABASE_URL)
    metadata = MetaData()
    
    active_tables = [
        "app_users",
        "app_url_scans",
        "app_message_scans",
        "app_password_resets",
        "app_feedback"
    ]
    
    with engine.connect() as conn:
        for table_name in active_tables:
            print(f"Backing up table: {table_name}")
            try:
                table = Table(table_name, metadata, autoload_with=engine)
                result = conn.execute(table.select())
            except Exception as e:
                print(f"Failed to reflect/read {table_name}: {e}")
                continue

            
            # Serialize rows to JSON
            rows = [dict(row._mapping) for row in result]
            
            # Convert datetime to string
            for row in rows:
                for k, v in row.items():
                    if hasattr(v, 'isoformat'):
                        row[k] = v.isoformat()
            
            backup_file = os.path.join(backup_dir, f"{table_name}.json")
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(rows, f, indent=2)
            print(f"Backed up {len(rows)} rows from {table_name}")
            
    print("MySQL backup completed safely.")

if __name__ == "__main__":
    backup_mysql()
