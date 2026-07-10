from pydantic import BaseModel

class StudentSchema(BaseModel):
    name : str
    age : int
    email : str
    city : str


class StudentUpdate(BaseModel):
    name : str = None
    age : str = None
    email : str = None
    city : str = None