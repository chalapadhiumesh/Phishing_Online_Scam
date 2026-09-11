from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from ..core.database import get_db
from .auth import get_current_user
from ..models.user import User
from ..models.url_scan import UrlScan
from ..models.message_scan import MessageScan

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("/urls")
def get_url_history(
    skip: int = 0, 
    limit: int = Query(20, le=100), 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    scans = db.query(UrlScan).filter(UrlScan.user_id == current_user.id).order_by(desc(UrlScan.timestamp)).offset(skip).limit(limit).all()
    total = db.query(UrlScan).filter(UrlScan.user_id == current_user.id).count()
    return {"total": total, "items": scans}

@router.get("/urls/{scan_id}")
def get_url_scan_detail(
    scan_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    scan = db.query(UrlScan).filter(UrlScan.id == scan_id, UrlScan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@router.get("/messages")
def get_message_history(
    skip: int = 0, 
    limit: int = Query(20, le=100), 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    scans = db.query(MessageScan).filter(MessageScan.user_id == current_user.id).order_by(desc(MessageScan.timestamp)).offset(skip).limit(limit).all()
    total = db.query(MessageScan).filter(MessageScan.user_id == current_user.id).count()
    return {"total": total, "items": scans}

@router.get("/messages/{scan_id}")
def get_message_scan_detail(
    scan_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    scan = db.query(MessageScan).filter(MessageScan.id == scan_id, MessageScan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@router.delete("/urls/{scan_id}")
def delete_url_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scan = db.query(UrlScan).filter(UrlScan.id == scan_id, UrlScan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    db.delete(scan)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return {"status": "success"}

@router.delete("/urls")
def delete_all_url_scans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(UrlScan).filter(UrlScan.user_id == current_user.id).delete()
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return {"status": "success"}
    
@router.delete("/messages/{scan_id}")
def delete_message_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scan = db.query(MessageScan).filter(MessageScan.id == scan_id, MessageScan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    db.delete(scan)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return {"status": "success"}

@router.delete("/messages")
def delete_all_message_scans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(MessageScan).filter(MessageScan.user_id == current_user.id).delete()
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return {"status": "success"}
