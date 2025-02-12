from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # 비밀번호는 해시 형태로 저장
    name = Column(String(100), nullable=False)  # 사용자 이름 추가
    age = Column(Integer, nullable=False)  # 나이 추가
    gender = Column(String(20), nullable=False)  # 성별 추가
    university = Column(String(255), nullable=False)  # 대학명 추가
    created_at = Column(DateTime, server_default=func.now())  # UTC 기준 생성 날짜