import os
from typing import Annotated

import argon2
import jwt
from dotenv import load_dotenv
from fastapi import Cookie, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.utils import get_expiration_time

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY", "thisisalongandrandomsecretkeyforthisstupidapp")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

ph = argon2.PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, plain)
        return True
    except Exception:
        return False


def create_access_token(data: dict, minutes_ttl: float = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = get_expiration_time(minutes_ttl)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None
):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        stmt = select(User).where(User.id == user_id)
        current_user = db.scalars(stmt).first()
        if not current_user:
            return RedirectResponse(url="/auth/login", status_code=302)
        return current_user

    except Exception:
        return RedirectResponse(url="/auth/login", status_code=302)


async def get_current_user_optional(
    db: Session = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None
):
    try:
        if not access_token:
            return None
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        stmt = select(User).where(User.id == user_id)
        current_user = db.scalars(stmt).first()
        return current_user
    except Exception:
        return None
