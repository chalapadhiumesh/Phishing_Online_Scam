from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..core.database import Base
from datetime import datetime

class PasswordReset(Base):
    __tablename__ = "app_password_resets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False)
    otp_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
