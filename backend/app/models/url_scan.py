from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class UrlScan(Base):
    __tablename__ = "app_url_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    url = Column(Text, nullable=False)
    prediction = Column(String(20), nullable=False) # 'phishing' or 'legitimate'
    confidence = Column(Float, nullable=False)
    risk_score = Column(Integer, nullable=False) # 0 to 100
    risk_level = Column(String(20), nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    indicators = Column(Text, nullable=True) # JSON string of features/indicators
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="url_scans")
