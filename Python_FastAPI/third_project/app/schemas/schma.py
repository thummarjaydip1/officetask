from pydantic import BaseModel
from datetime import date
from typing import Optional

class PersonSchema(BaseModel):
    name : str
    email : str
    address : str
    birth_date : date


class PersonSchemaUpdate(BaseModel):
    name : str = None
    email : str = None 
    address : str = None 
    birth_date : date = None


class PersonSchemaDisplay(BaseModel):
    id : int
    name : str
    email : str
    address : str
    birth_date : date