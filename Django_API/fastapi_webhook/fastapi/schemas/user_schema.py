from pydantic import BaseModel, Field
from datetime import datetime
# from typing import Optional

# class RegisterUser(BaseModel):
#     username : str
#     password : str = Field(min_length=3, max_length=50)
#     email : str
#     address : str
    # address : Optional[str] = None

# class LoginUser(BaseModel):
#     username : str
#     password : str = Field(min_length=3, max_length=50)

class DisplayUser(BaseModel):
    id : int
    username : str
    password : str
    email : str
    address : str
    image : str
    create_at : datetime

    class config:
        from_attributes = True

# class UpdateUser(BaseModel):
#     username : str
#     password : str = Field(min_length=3, max_length=50)
#     email : str
#     address : str 

# ***** Nested Model *****  -->(--Address model include in User Model--)
# class Address(BaseModel):
#     city : str
#     state : str
#                               
# class User(BaseModel):
#     name : str
#     address : Address

