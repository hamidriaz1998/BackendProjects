from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_utils import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.db import get_db
from app.models import User
from app.schemas import (
    GetUserDTO,
    UserRegisterDTO,
)
from app.templates import templates

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/register")
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_form_submit(
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    stmt = select(User).where(User.email == email).where(User.username == username)
    if db.scalars(stmt).first():
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email or username already exists"},
        )

    new_user = User(
        email=email,
        username=username,
        password=hash_password(password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auto login after registration
    token_data = {"sub": str(new_user.id)}
    token = create_access_token(token_data)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@router.post("/register/api", response_model=GetUserDTO)
async def register_api(
    user: UserRegisterDTO,
    db: Session = Depends(get_db),
):
    stmt = (
        select(User)
        .where(User.email == user.email)
        .where(User.username == user.username)
    )
    if db.scalars(stmt).first():
        raise HTTPException(status_code=400, detail="Email or username already exists")

    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    stmt = select(User).where(User.email == email)
    current_user = db.scalars(stmt).first()
    if not current_user or not verify_password(password, current_user.password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid Credentials"}
        )

    token_data = {"sub": str(current_user.id)}
    token = create_access_token(token_data)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response


@router.get("/me", response_model=GetUserDTO)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/refresh_token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    token_data = {"sub": current_user.id}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}
