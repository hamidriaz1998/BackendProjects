from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,  # noqa: F401
)
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.auth_utils import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    generate_otp,
    hash_password,
    verify_otp,
    verify_password,
)
from app.db import get_db
from app.email_handler import EmailHandler, EmailType
from app.models import User, UserOTP
from app.schemas import GetUserDTO, UserLoginDTO, UserOTPVerify, UserRegisterDTO
from app.utils import get_expiration_time

router = APIRouter(prefix="/auth", tags=["Auth"])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login", refreshUrl="/user/refresh_token")
http_bearer = HTTPBearer()


@router.post("/register", response_model=GetUserDTO)
async def register(
    user: UserRegisterDTO,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    stmt = (
        select(User)
        .where(User.email == user.email)
        .where(User.username == user.username)
    )
    if db.scalars(stmt).first():
        raise HTTPException(status_code=400, detail="Email or username already exists")

    with db.begin():
        new_user = User(
            email=user.email,
            username=user.username,
            password=hash_password(user.password),
        )
        db.add(new_user)
        db.flush()  # Flush to get the ID without committing

        # Generate OTP
        expiry_in_minutes = 10
        otp = UserOTP()
        otp.otp = generate_otp()
        otp.expiration = get_expiration_time(after_minutes=expiry_in_minutes)
        otp.user_id = new_user.id

        db.add(otp)

    db.refresh(new_user)
    db.refresh(otp)

    email_handler = EmailHandler()
    background_tasks.add_task(
        email_handler.send_email,
        receiver=user.email,
        email_type=EmailType.OTP,
        otp=otp.otp,
        valid_time=f"{expiry_in_minutes} minutes",
        username=user.username
    )

    return new_user


@router.post("/verify")
async def verify(data: UserOTPVerify, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    current_user = db.scalars(stmt).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    stmt = select(UserOTP).where(UserOTP.user_id == current_user.id)
    current_otp = db.scalars(stmt).first()
    if not current_otp or not verify_otp(current_otp, data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    with db.begin():
        current_otp.used = True
        current_user.verified = True
    db.refresh(current_user)
    token_data = {"sub": str(current_user.id)}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/request-otp")
def request_otp(
    email: EmailStr, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    stmt = select(User).where(User.email == email)
    current_user = db.scalars(stmt).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    expiry_in_minutes = 10
    otp = generate_otp()
    stmt = (
        update(UserOTP)
        .where(UserOTP.user_id == current_user.id)
        .values(otp=otp, used=False, expiration=get_expiration_time(expiry_in_minutes))
    )
    db.execute(stmt)
    db.commit()
    db.refresh(current_user)

    email_handler = EmailHandler()
    background_tasks.add_task(
        email_handler.send_email,
        receiver=current_user.email,
        email_type=EmailType.OTP,
        otp=otp,
        valid_time=f"{expiry_in_minutes} minutes",
        username=current_user.username
    )
    return {"message": "OTP sent"}


@router.post("/login")
async def login(user: UserLoginDTO, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    current_user = db.scalars(stmt).first()
    if not current_user or not verify_password(user.password, current_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not current_user.verified:
        raise HTTPException(status_code=403, detail="User not verified")
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
