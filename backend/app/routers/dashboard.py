from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..core.database import get_db
from ..models.url_scan import UrlScan
from ..models.message_scan import MessageScan
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # URL Stats
    url_scans_query = db.query(UrlScan).filter(UrlScan.user_id == current_user.id)
    total_url_scans = url_scans_query.count()
    url_phishing = url_scans_query.filter(UrlScan.prediction == 'phishing').count()
    url_legit = total_url_scans - url_phishing

    # Message Stats
    msg_scans_query = db.query(MessageScan).filter(MessageScan.user_id == current_user.id)
    total_msg_scans = msg_scans_query.count()
    msg_scam = msg_scans_query.filter(MessageScan.prediction == 'scam').count()
    msg_legit = total_msg_scans - msg_scam

    # High Risk
    high_risk_urls = url_scans_query.filter(UrlScan.risk_level.in_(['HIGH', 'CRITICAL'])).count()
    high_risk_msgs = msg_scans_query.filter(MessageScan.risk_level.in_(['HIGH', 'CRITICAL'])).count()

    return {
        "url_scans": {
            "total": total_url_scans,
            "phishing": url_phishing,
            "legitimate": url_legit
        },
        "message_scans": {
            "total": total_msg_scans,
            "scam": msg_scam,
            "legitimate": msg_legit
        },
        "high_risk_total": high_risk_urls + high_risk_msgs,
        "total_scans": total_url_scans + total_msg_scans,
        "total_phishing": url_phishing + msg_scam
    }
