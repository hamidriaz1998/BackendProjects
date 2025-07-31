import datetime
import os
import random

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

from app.models.auth.Userotp import UserOTP
from app.utils import get_expiration_time

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY", "thisisalongandrandomsecretkeyforthisstupidapp")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, minutes_ttl: float = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = get_expiration_time(minutes_ttl)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def generate_otp(digits: int = 8) -> int:
    return random.randint(10 ** (digits - 1), 10**digits - 1)


def verify_otp(otp: UserOTP, input_otp: int) -> bool:
    return otp.otp == input_otp and otp.expiration > datetime.datetime.now(
        datetime.timezone.utc
    )
