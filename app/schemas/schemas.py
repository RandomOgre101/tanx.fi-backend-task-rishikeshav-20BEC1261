from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


# Schema for creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for response of a user's information
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Schema for status row of Alert table to be of type ENUM
class AlertStatusEnum(str, Enum):
    created = "created"
    deleted = "deleted"
    triggered = "triggered"

# Schema for creating an alert
class AlertCreate(BaseModel):
    status: Optional[AlertStatusEnum] = "created"
    crypto_name: str
    price_to_alert: int

# Schema for response of an alert
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