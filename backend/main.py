from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import UserLogin, Token, UserCreate
from crud import authenticate_user, get_user_by_email, create_user, verify_password
from auth import create_access_token, decode_access_token
from fastapi.middleware.cors import CORSMiddleware
from models import User

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)
app = FastAPI()
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# CORS 설정 (프론트엔드와 연동할 경우 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # 프론트엔드 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """사용자 로그인"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/signup")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입 API"""
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    현재 로그인한 사용자 정보를 반환하는 API.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_email = payload["sub"]
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "username": user.username, "email": user.email}


@app.post("/auth/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    이메일과 비밀번호를 받아 로그인하는 엔드포인트.
    """
    # 1. email로 사용자 검색
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 2. 비밀번호 검증
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 3. 토큰 생성 (JWT 등)
    access_token = create_access_token(data={"sub": user.email})
    
    # 4. 토큰 반환
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    