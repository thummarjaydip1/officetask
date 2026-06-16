from pydantic import BaseModel

class CreateUser(BaseModel):
    username : str
    password : str
    email : str

class LoginUser(BaseModel):
    username : str
    password : str

class UpdateUser(BaseModel):
    username : str
    password : str
    email : str