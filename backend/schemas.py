# Structure of Datas
from pydantic import BaseModel, EmailStr
from enum import Enum

class GenderEnum(str, Enum):
    male = "남성"
    female = "여성"
    tyrannosaurus = "티라노사우르스"
    helicopter = "헬리콥터"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int
    gender: GenderEnum
    University: str
    username: str


class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
