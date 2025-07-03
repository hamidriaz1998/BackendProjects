from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime


class UserRegisterDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class GetUserDTO(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class CreateUrlDTO(BaseModel):
    original_url: HttpUrl
    ttl_minutes: float

    class Config:
        from_attributes = True


class GetUrlDTO(BaseModel):
    original_url: str
    short_url: str
    click_count: int
    expires_at: datetime

    class Config:
        from_attributes = True
