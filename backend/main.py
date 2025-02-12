import sys
import os

# 현재 파일(`main.py`)의 디렉토리를 기준으로 `backend/` 경로를 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import auth_r  # ✅ auth 라우터 불러오기

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_r.router)