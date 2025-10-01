from pydantic import BaseModel, Field, field_validator
from typing import Union, Annotated
from datetime import datetime
from decimal import Decimal
from typing import Optional




class PaymentSchema(BaseModel):
    id: int
    amount: Optional[Decimal] = None
    created_at: datetime
    description: Optional[str] = None




class PaymentCreateSchema(BaseModel):
    description: Annotated[str, Field(min_length=10, max_length=255)]
    amount : Decimal



    @field_validator("amount")
    def validate_amount_is_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v
    



class PaymentUpdateSchema(BaseModel):
    description: Annotated[str, Field(min_length=10, max_length=255)]
    amount : Decimal


    @field_validator("amount")
    def validate_amount_is_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v