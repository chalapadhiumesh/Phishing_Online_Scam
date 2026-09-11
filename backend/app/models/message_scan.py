from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class MessageScan(Base):
    __tablename__ = "app_message_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    message_text = Column(Text, nullable=False)
    prediction = Column(String(20), nullable=False) # 'scam' or 'legitimate'
    confidence = Column(Float, nullable=False)
    risk_score = Column(Integer, nullable=False) # 0 to 100
    risk_level = Column(String(20), nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    indicators = Column(Text, nullable=True) # JSON string of features/indicators
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="message_scans")
