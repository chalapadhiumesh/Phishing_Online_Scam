from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Any
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings
from ..models.user import User, UserRole
from pydantic import BaseModel, EmailStr, ConfigDict
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from ..models.password_reset import PasswordReset
import smtplib
from email.message import EmailMessage
import secrets
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class GoogleAuthRequest(BaseModel):
    token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import JWTError, jwt
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    if not getattr(user, 'is_active', True):
        raise HTTPException(status_code=400, detail='Inactive user')
    return user

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    user_by_email = db.query(User).filter(User.email == user_in.email).first()
    if user_by_email:
        raise HTTPException(status_code=400, detail="An account with this email already exists. Please log in instead.")
        
    # Check if username exists
    user_by_username = db.query(User).filter(User.username == user_in.username).first()
    if user_by_username:
        raise HTTPException(status_code=400, detail="This username is already taken. Please choose another username.")
        
    if len(user_in.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    try:
        db.commit()
        if hasattr(db, 'refresh'): db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/google")
def google_auth(req: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        # If GOOGLE_CLIENT_ID is empty (dev mode), we still verify if it's a valid token structure 
        # But for real production, it MUST verify against the client id.
        if not settings.GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=500, detail="Google Auth not configured")
        
        client_id = settings.GOOGLE_CLIENT_ID
        
        idinfo = id_token.verify_oauth2_token(req.token, google_requests.Request(), client_id)
        email = idinfo['email']
        username = email.split('@')[0]
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Create new user
            base_username = username
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{base_username}{counter}"
                counter += 1
                
            hashed_password = get_password_hash("random_generated_oauth_password_placeholder")
            user = User(
                username=username,
                email=email,
                password_hash=hashed_password
            )
            db.add(user)
            try:
                db.commit()
                if hasattr(db, 'refresh'): db.refresh(user)
            except Exception:
                db.rollback()
                raise HTTPException(status_code=500, detail='Database transaction failed')
            
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Google token: {str(e)}")

def send_otp_email(to_email: str, otp: str):
    print(f"MOCK SMTP: Sending OTP email to {to_email}")
    try:
        msg = EmailMessage()
        msg.set_content(f"Your password reset OTP is: {otp}\nIt expires in 15 minutes.")
        msg['Subject'] = 'ScamShield AI Password Reset'
        msg['From'] = 'noreply@scamshield-ai.com'
        msg['To'] = to_email
        # Mocked for now to avoid SMTP connection errors in dev.
    except Exception as e:
        print(f"SMTP Error: {e}")

@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        return {"message": "If an account with that email exists, an OTP has been sent."}
        
    otp = secrets.token_hex(3).upper() # 6-char hex string
    otp_hash = get_password_hash(otp)
    
    expires = datetime.utcnow() + timedelta(minutes=15)
    
    # Delete old resets
    db.query(PasswordReset).filter(PasswordReset.user_id == user.id).delete()
    
    reset_entry = PasswordReset(user_id=user.id, otp_hash=otp_hash, expires_at=expires)
    db.add(reset_entry)
    try:
        db.commit()
        if hasattr(db, 'refresh'): db.refresh(reset_entry)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    
    send_otp_email(user.email, otp)
    
    return {"message": "If an account with that email exists, an OTP has been sent."}

@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")
        
    reset_entry = db.query(PasswordReset).filter(PasswordReset.user_id == user.id).first()
    if not reset_entry:
        raise HTTPException(status_code=400, detail="No active reset request")
        
    if reset_entry.expires_at < datetime.utcnow():
        db.delete(reset_entry)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Database transaction failed')
        raise HTTPException(status_code=400, detail="OTP has expired")
        
    if not verify_password(req.otp, reset_entry.otp_hash):
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    if len(req.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
    user.password_hash = get_password_hash(req.new_password)
    db.delete(reset_entry)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail='Database transaction failed')
    
    return {"message": "Password reset successful"}
