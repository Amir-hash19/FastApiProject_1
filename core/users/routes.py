from core.auth.auth_jwt import generate_access_token, generate_refresh_token, decode_refresh_token, get_authenticated_user
from fastapi import FastAPI, status, HTTPException, Path, Request,Response,Depends, APIRouter
from fastapi.responses import JSONResponse, Response
from core.users.models import pwd_context
from core.users.models import User
from sqlalchemy.orm import Session
from core.database import get_db
from pydantic import BaseModel
from typing import Optional
import random

from .schemas import UserBaseSchema, UserloginSchema, DeleteAccountSchema

router = APIRouter(prefix="/api/v1")    



"""the endpoint will created an account for user and assign tokens"""
@router.post("/register")
async def user_register(request: UserBaseSchema,db:Session = Depends(get_db)):
    if db.query(User).filter_by(email=request.email.lower()).first():
                raise HTTPException(
                     status_code=status.HTTP_409_CONFLICT, detail="email already exists")
    
    user_obj = User(email=request.email.lower(),
            full_name=request.full_name,
            national_id=request.national_id)  
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)    

    return JSONResponse(
            content={
                "detail": "user registered successfully",
                "access": access_token,
                "refresh": refresh_token,
            },
            status_code=status.HTTP_201_CREATED,
    )





"""this is an API for login and take an access token"""

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def user_login(
    request: UserloginSchema,
    response: Response,
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter_by(email=request.email.lower()).first()

    if not user or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    access_token = generate_access_token({"sub": str(user.id)})
    refresh_token = generate_refresh_token({"sub": str(user.id)})

 
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,       
        secure=True,          
        samesite="lax",       
        max_age=7 * 24 * 60 * 60,  
        path="/auth",         
    )


    return {
        "detail": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }




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
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400,
        path="/"
    )

    return {"msg": "Tokens refreshed"}






@router.delete("/you", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    request: DeleteAccountSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user)
):
    
    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )


    db.delete(user)
    db.commit()

    return None  
