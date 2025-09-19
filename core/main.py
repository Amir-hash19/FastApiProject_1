from fastapi import FastAPI, status, HTTPException, Path
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional
import random

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
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")



class PaymentUpdate(BaseModel):
    description: str
    amount: float 


@app.put("/payments/{payment_id}")
def edit_payment(
    payment_id: int = Path(title="Payment ID", description="The ID of the Payment"),
    payment: PaymentUpdate = None,               
):
    """This api for returning updated object"""
    if payment_id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    data[payment_id] = {
        "description": payment.description,
        "amount": payment.amount
    }
    return {"message":"Payment Updated successfully", "Payment":data[payment_id]}
    
    
    
class PaymentUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None






class Payment(BaseModel):
    description: str
    amount: float

@app.post("/payment/create/")
def create_payment(payment: Payment):
    """the endpoint creates a new payment and stores it in the 'data' dictionary"""
   
    new_id = random.randint(3, 99)
    data[new_id] = {"description": payment.description, "amount": payment.amount}

    return JSONResponse(
        content={
            "message": "Payment created successfully",
            "id": new_id,
            "payment": data[new_id]
        },
        status_code=status.HTTP_201_CREATED
    )





@app.delete("/payment/{payment_id}")
def delete_payment(payment_id: int):
    if payment_id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    deleted = data.pop(payment_id)
    return JSONResponse({"message": "Payment deleted successfully", "deleted_payment": deleted}, status_code=status.HTTP_204_NO_CONTENT)