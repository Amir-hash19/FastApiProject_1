from fastapi import FastAPI, status, HTTPException, Path, Request,Response,Depends
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional
import random
from core.database import User,Payment,get_db
from sqlalchemy.orm import Session
from core.database import pwd_context
from core.auth.auth_jwt import generate_access_token, generate_refresh_token, decode_refresh_token


from core.schemas import PaymentCreateSchema, PaymentUpdateSchema



app = FastAPI()

data = {
    1:{
        "description":"payed for rent",
        "amount":100
    },

    2:{
        "description":"payed for car ",
        "amount":1000
    }
    
}



@app.get("/payments")
def get_payments():

    """ This API return all of the payments in form of the json response """

    return JSONResponse(content=data, status_code=status.HTTP_200_OK)



@app.get("/payment/{payment_id}")
def retrieve_payment_detail(payment_id: int = Path(title="payment id"
                            ,description="The id of the Payment in data")):
    
    """this endpoint takes payment id and return the values of that"""

    if payment_id in data:
        return data[payment_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")




@app.put("/payments/{payment_id}")
def edit_payment(
    payment: PaymentUpdateSchema, payment_id: int = Path(title="Payment ID", description="The ID of the Payment"),
):
    """This api for returning updated object"""
    if payment_id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    data[payment_id] = {
        "description": payment.description,
        "amount": payment.amount
    }
    return {"message":"Payment Updated successfully", "Payment":data[payment_id]}
    
    






# class Payment(BaseModel):
#     description: str
#     amount: float

@app.post("/payment/create/")
def create_payment(payment: PaymentCreateSchema):
    """the endpoint creates a new payment and stores it in the 'data' dictionary"""
   
    new_id = random.randint(3, 99)
    data[new_id] = {"description": payment.description, "amount": payment.amount}

    return JSONResponse(
        content={
            "message": "Payment created successfully",
            "description": payment.description,
            "payment" : new_id
        },
        status_code=status.HTTP_201_CREATED
    )





@app.delete("/payment/{payment_id}")
def delete_payment(payment_id: int):
    if payment_id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    deleted = data.pop(payment_id)
    return JSONResponse({"message": "Payment deleted successfully", "deleted_payment": deleted}, status_code=status.HTTP_204_NO_CONTENT)


"""
endpoint for authentication users and setcookies 
"""


# -----------------------
# 1. LOGIN
# -----------------------
@app.post("/login")
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


# -----------------------
# 2. REFRESH
# -----------------------
@app.post("/refresh")
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


# -----------------------
# 3. LOGOUT
# -----------------------
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"msg": "Logged out"}
