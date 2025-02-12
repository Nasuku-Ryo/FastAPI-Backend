import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 데이터베이스 URL 가져오기 (None 방지)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:0000@localhost:3306/mydatabase")

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL, echo=False)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델을 위한 Base 클래스
Base = declarative_base()

# DB 세션을 생성하고 관리하는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
