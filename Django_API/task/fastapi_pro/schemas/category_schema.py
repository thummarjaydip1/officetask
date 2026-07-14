from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name : str

class CategoryDisplay(BaseModel):
    id : int
    name : str


# class Image(BaseModel):
#     url : str
#     name : str

# class newSchemas(BaseModel):
#     name : str = Field(default=None, examples=["manan"], max_length=500)
#     price : float = Field(gt = 0, description = "price must be greater than zero")
#     tax : float | None = None 
#     tags : list[str] = []
#     image : Image | None = None
#     limit : int = Field(gt = 0 , le = 100)