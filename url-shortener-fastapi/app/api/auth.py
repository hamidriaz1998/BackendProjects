from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,  # noqa: F401
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_utils import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)
from app.db import get_db
from app.models import User
from app.schemas import GetUserDTO, UserLoginDTO, UserRegisterDTO

router = APIRouter(prefix="/user", tags=["User"])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login", refreshUrl="/user/refresh_token")
http_bearer = HTTPBearer()


@router.post("/register", response_model=GetUserDTO)
async def register(user: UserRegisterDTO, db: Session = Depends(get_db)):
    stmt = (
        select(User)
        .where(User.email == user.email)
        .where(User.username == user.username)
    )
    if db.scalars(stmt).first():
        raise HTTPException(status_code=400, detail="Email or username already exists")
    new_user = User(
        email=user.email, username=user.username, password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user: UserLoginDTO, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    current_user = db.scalars(stmt).first()
    if not current_user or not verify_password(user.password, current_user.password):  # pyright: ignore
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"sub": str(current_user.id)}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(
    db: Session = Depends(get_db),
    # token: str = Depends(oauth2_scheme)
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        stmt = select(User).where(User.id == user_id)
        current_user = db.scalars(stmt).first()
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        return current_user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/me", response_model=GetUserDTO)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/refresh_token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    token_data = {"sub": current_user.id}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}
