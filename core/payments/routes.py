from core.auth.auth_jwt import generate_access_token, generate_refresh_token, decode_refresh_token,get_authenticated_user
from fastapi import FastAPI, status, HTTPException, Path, Request,Response,Depends,APIRouter, Query
from fastapi.responses import JSONResponse
from core.users.models import User
from core.payments.models import Payment
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
import random

from .schemas import PaymentSchema, PaymentCreateSchema, PaymentUpdateSchema

router = APIRouter(prefix="/api/v1")



@router.get("/payments", response_model=List[PaymentSchema])
async def retrieve_payment_list(
    db: Session = Depends(get_db),                    
    user: User = Depends(get_authenticated_user),    
    limit: int | None = Query(default=None,           
                               description="limiting the number of items to retrieve")
):
    """this endpoint will return all of the user payments"""
    query = db.query(Payment).filter(Payment.user_id == user.id)

    if limit:
        query = query.limit(limit)

    payments = query.all()
    return payments    





@router.post("/payments", response_model=PaymentSchema)
async def create_payment(request: PaymentCreateSchema, db:Session = Depends(get_db), user: User = Depends(get_authenticated_user)):
    """this endpoint will create a payement object for user"""
    data = request.model_dump()
    data.update({"user_id":user.id})
    payment = Payment(**data)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment





@router.get("/payments/{payment_id}", response_model=PaymentSchema)
async def retrieve_payment(
    payment_id: int ,
    db: Session = Depends(get_db),           # پارامتر با مقدار پیش‌فرض
    user: User = Depends(get_authenticated_user),  # پارامتر با مقدار پیش‌فرض
                             
):
    payment_obj = db.query(Payment).filter(
    Payment.id == payment_id,
    Payment.user_id == user.id
    ).first()

    if not payment_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    return payment_obj
    




@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: int = Path(...,gt=0),
    db: Session = Depends(get_db), 
    user: User = Depends(get_authenticated_user)
):
    del_payment = db.query(Payment).filter(
    Payment.id == payment_id,
    Payment.user_id == user.id
    ).first()

    if not del_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    db.delete(del_payment)
    db.commit()
    return JSONResponse(content={"detail":"Payment deleted Successfully"})
    




@router.put("/payments/{payment_id}", response_model=PaymentSchema)
async def update_payment(
    payment_id: int,
    payment_data: PaymentUpdateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user)
):
    """ updating an object element """
    
    payment_obj = db.query(Payment).filter(
        Payment.id == payment_id,
        Payment.user_id == user.id
    ).first()

    if not payment_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    if payment_data.amount is not None:
        payment_obj.amount = payment_data.amount
    if payment_data.description is not None:
        payment_obj.description = payment_data.description

    db.commit()
    db.refresh(payment_obj)

    return payment_obj

