from pydantic import BaseModel

class NotificationSchema(BaseModel):
    user_id: int
    message: str

class NotificationDisplaySchemas(BaseModel):
    id : int
    user_id :  int
    message : str