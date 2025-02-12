from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # ✅ 상대 경로(`..database`) 대신 절대 경로 사용
from schemas import UserLogin, Token, UserCreate  # ✅ 절대 경로 사용
from crud import authenticate_user, get_user_by_email, create_user, verify_password 
from auth import create_access_token, decode_access_token 
from models import User
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입 API"""
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/auth/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """이메일과 비밀번호를 받아 로그인하는 API"""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """현재 로그인한 사용자 정보 반환"""
    payload = decode_access_token(token)  
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_email = payload["sub"]
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "username": user.username, "email": user.email}