from pydantic import BaseModel, EmailStr


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


class UserOTPVerify(BaseModel):
    email: EmailStr
    otp: int
