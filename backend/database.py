from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 연결 정보 
DATABASE_URL = "mysql+pymysql://root:0000@localhost:3306/mydatabase"

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

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
