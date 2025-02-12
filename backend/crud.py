from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin
from passlib.context import CryptContext

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create (회원가입)
def create_user(db: Session, user: UserCreate):
    """새로운 사용자 생성"""
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        age=user.age,
        gender=user.gender,
        university=user.University,  # 필드 이름 일치
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read (로그인 인증)
def authenticate_user(db: Session, email: str, password: str):
    """이메일과 비밀번호로 사용자 인증"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

# Read (이메일로 사용자 찾기)
def get_user_by_email(db: Session, email: str):
    """이메일을 기준으로 사용자 정보 조회"""
    return db.query(User).filter(User.email == email).first()