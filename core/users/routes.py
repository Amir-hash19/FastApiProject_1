from core.auth.auth_jwt import generate_access_token, generate_refresh_token, decode_refresh_token
from fastapi import FastAPI, status, HTTPException, Path, Request,Response,Depends, APIRouter
from fastapi.responses import JSONResponse, Response
from core.users.models import pwd_context
from core.users.models import User
from sqlalchemy.orm import Session
from core.database import get_db
from pydantic import BaseModel
from typing import Optional
import random



router = APIRouter(prefix="/api/v1")






@router.post("/login")
def login(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)


    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=300,  # 5 دقیقه
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400,  # 1 روز
        path="/"
    )

    return {"msg": "Login successful"}



@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    user_id = decode_refresh_token(refresh_token) 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    new_access = generate_access_token(user.id)
    new_refresh = generate_refresh_token(user.id)


    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=300,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400,
        path="/"
    )

    return {"msg": "Tokens refreshed"}



@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"msg": "Logged out"}
