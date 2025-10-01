from pydantic import BaseModel, Field, field_validator
from typing import Union, Annotated


class PaymentCreateSchema(BaseModel):
    description: Annotated[str, Field(min_length=10, max_length=255)]
    amount : Union[int, float]


    @field_validator("amount")
    def validate_amount_is_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return 
    



class PaymentUpdateSchema(BaseModel):
    description: Annotated[str, Field(min_length=10, max_length=255)]
    amount : Union[int, float]


    @field_validator("amount")
    def validate_amount_is_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v