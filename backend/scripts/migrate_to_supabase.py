import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, MetaData, Table
from backend.app.core.config import settings
from backend.app.core.database import Base

# ensure models are registered
from backend.app.models.user import User
from backend.app.models.url_scan import UrlScan
from backend.app.models.message_scan import MessageScan
from backend.app.models.feedback import Feedback
from backend.app.models.password_reset import PasswordReset

def migrate():
    print("Starting Migration from MySQL to Supabase...")
    
    mysql_engine = create_engine(settings.DATABASE_URL)
    supabase_engine = create_engine(settings.SUPABASE_DATABASE_URL)
    
    print("Creating tables in Supabase (if they don't exist)...")
    Base.metadata.create_all(bind=supabase_engine)
    print("Schema initialized.")
    
    tables_to_migrate = [
        User.__tablename__,
        UrlScan.__tablename__,
        MessageScan.__tablename__,
        Feedback.__tablename__,
        PasswordReset.__tablename__
    ]
    
    mysql_metadata = MetaData()
    supabase_metadata = MetaData()
    
    migration_report = []
    
    with mysql_engine.connect() as mysql_conn:
        with supabase_engine.connect() as sup_conn:
            with sup_conn.begin():
                for table_name in tables_to_migrate:
                    print(f"\nMigrating {table_name}...")
                    
                    try:
                        mysql_table = Table(table_name, mysql_metadata, autoload_with=mysql_engine)
                        sup_table = Table(table_name, supabase_metadata, autoload_with=supabase_engine)
                    except Exception as e:
                        print(f"Skipping {table_name}: {e}")
                        continue
                    
                    # Fetch
                    mysql_result = mysql_conn.execute(mysql_table.select())
                    rows = [dict(row._mapping) for row in mysql_result]
                    mysql_count = len(rows)
                    
                    if mysql_count > 0:
                        # Clear target just in case (to avoid duplicate PKs during multiple migration attempts)
                        sup_conn.execute(sup_table.delete())
                        
                        # Insert
                        sup_conn.execute(sup_table.insert(), rows)
                    
                    # Verify
                    sup_result = sup_conn.execute(sup_table.select())
                    sup_count = len(list(sup_result))
                    
                    status = "PASS" if mysql_count == sup_count else "FAIL"
                    diff = mysql_count - sup_count
                    migration_report.append({
                        "table": table_name,
                        "mysql_rows": mysql_count,
                        "sup_rows": sup_count,
                        "diff": diff,
                        "status": status
                    })
                    print(f"{table_name}: MySQL={mysql_count}, Supabase={sup_count} -> {status}")
                    
    # Generate Report
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "supabase-migration-verification.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Supabase Migration Verification Report\n\n")
        f.write("| Table | MySQL Rows | Supabase Rows | Difference | Status |\n")
        f.write("|---|---|---|---|---|\n")
        for r in migration_report:
            f.write(f"| {r['table']} | {r['mysql_rows']} | {r['sup_rows']} | {r['diff']} | {r['status']} |\n")
            
    print("\nMigration complete! Report generated at docs/supabase-migration-verification.md")

if __name__ == "__main__":
    migrate()
