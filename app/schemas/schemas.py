from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class AlertStatusEnum(str, Enum):
    created = "created"
    deleted = "deleted"
    triggered = "triggered"

class AlertCreate(BaseModel):
    status: Optional[AlertStatusEnum] = "created"
    crypto_name: str
    price_to_alert: int

class AlertOut(BaseModel):
    id: int
    status: str
    crypto_name: str
    price_to_alert: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostDelete(BaseModel):
    status: str = "deleted"


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None