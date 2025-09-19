from fastapi import FastAPI, status, HTTPException, Path
from fastapi.responses import JSONResponse
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
    if payment_id in data:
        return data[payment_id]
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
