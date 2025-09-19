from fastapi import FastAPI, status, HTTPException
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
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)