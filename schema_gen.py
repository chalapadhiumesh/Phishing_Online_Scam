from sqlalchemy.schema import CreateTable
from backend.app.core.database import engine
from backend.app.models.user import User
from backend.app.models.url_scan import UrlScan
from backend.app.models.message_scan import MessageScan
from backend.app.models.feedback import Feedback

def generate_schema():
    with open("database_schema.sql", "w") as f:
        for model in [User, UrlScan, MessageScan, Feedback]:
            create_stmt = CreateTable(model.__table__).compile(engine)
            f.write(str(create_stmt) + ";\n\n")

if __name__ == "__main__":
    generate_schema()
