from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
import json
from ..core.database import get_db
from .auth import get_current_user
from ..models.user import User
from ..models.url_scan import UrlScan
from ..models.message_scan import MessageScan
from ..services.ml_service import ml_service

router = APIRouter(prefix="/api/scan", tags=["scan"])

class URLScanRequest(BaseModel):
    url: str = Field(..., max_length=2048)

class MessageScanRequest(BaseModel):
    message: str = Field(..., max_length=10000)

@router.post("/url")
def scan_url(request: URLScanRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = ml_service.predict_url(request.url)
    
    new_scan = UrlScan(
        user_id=current_user.id,
        url=request.url,
        prediction=result["prediction"],
        confidence=result["confidence"],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        indicators=json.dumps(result["indicators"])
    )
    db.add(new_scan)
    try:
        db.commit()
        if hasattr(db, 'refresh'):
            db.refresh(new_scan)
    except Exception as e:
        print(f"Database error during URL scan insert: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return new_scan

@router.post("/message")
def scan_message(request: MessageScanRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = ml_service.predict_message(request.message)

    new_scan = MessageScan(
        user_id=current_user.id,
        message_text=request.message,
        prediction=result["prediction"],
        confidence=result["confidence"],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        indicators=json.dumps(result["indicators"])
    )
    db.add(new_scan)
    try:
        db.commit()
        if hasattr(db, 'refresh'):
            db.refresh(new_scan)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return new_scan
