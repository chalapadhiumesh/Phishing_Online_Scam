from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Feedback(Base):
    __tablename__ = "app_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    scan_type = Column(String(20), nullable=False) # 'url' or 'message'
    scan_id = Column(Integer, nullable=False) # The ID in the corresponding table
    is_accurate = Column(Boolean, nullable=False)
    comments = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="feedbacks")
