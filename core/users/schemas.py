from pydantic import BaseModel, Field, field_validator



class UserBaseSchema(BaseModel):
    email: str = Field(
        ...,max_length=170,description="use email for validate user"
    )
    full_name: str = Field(
        ...,max_length=200,description="set fullname for user"
    )
    national_id: str = Field(...,max_length=10,min_length=0)
    password: str = Field(max_length=70, min_length=8)
    password_confirm: str = Field(max_length=70,min_length=8,
    description="password confirmation")


    @field_validator("password_confirm")
    def check_passwords_match(cls, password_confirm, validation):
        if not (password_confirm == validation.data.get("password")):
            raise ValueError("passwords invalid")
        return password_confirm




class UserloginSchema(BaseModel):
    email: str = Field(..., max_length=128, description="email of the user")
    password: str = Field(..., max_length=70, min_length=8)





class DeleteAccountSchema(BaseModel):
    password: str