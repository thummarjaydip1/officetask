from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import Notification
from schemas.notification_schema import NotificationSchema

router = APIRouter(
    prefix = "/webhook",
    tags = ["Notification"]
)

@router.post("/notification/add")
def webhook_notification_add(data : NotificationSchema, db : Session = Depends(get_db)):
    new_notification = Notification(
        user_id = data.user_id,
        message = data.message
    )
    
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return {
        'message' : "webhook notification receive successfully",
        "notification_id" : new_notification.id
    }