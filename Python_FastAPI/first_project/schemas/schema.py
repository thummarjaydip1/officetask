from pydantic import BaseModel

class StudentSchema(BaseModel):
    name : str
    age : int
    city : str

 
class StudentDisplay(BaseModel):
    id : int
    name : str
    age : int
    city : str


# class Student(BaseModel):
#     name : str | None = None
#     age : int | None = None
#     city : str | None = None
#     is_active : bool
