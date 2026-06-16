from pydantic import BaseModel

class CreateStudent(BaseModel):
    name : str
    email : str
    city : str

class DispStudent(BaseModel):
    id : int
    name : str
    email : str
    city : str

    class config():
        from_attributes = True

class UpdateStudent(BaseModel):
    name : str
    email : str
    city : str
    