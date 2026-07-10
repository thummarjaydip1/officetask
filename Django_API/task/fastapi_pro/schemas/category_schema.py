from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name : str

class CategoryDisplay(BaseModel):
    id : int
    name : str