from pydantic import BaseModel

class Contact(BaseModel):
    name : str
    age : int
    email : str
    city : str