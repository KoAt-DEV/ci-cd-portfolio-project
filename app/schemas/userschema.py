from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from typing import Optional
import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str]


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class MeResponse(BaseModel):
    user_name: str
    user_email: str
    user_created_at: datetime.datetime
