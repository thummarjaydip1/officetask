from pydantic import BaseModel

class BillSchemas(BaseModel):
    order_id : int
    customer_name : str
    product_name : str
    price : int
    quantity : int
    total_price : int   

class BillSchemasUpdate(BaseModel):
    quantity : int
    total_price : int