from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import Notification
from schemas.notification_schema import NotificationSchema, NotificationDisplaySchemas

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


@router.get("/notification/display", response_model = list[NotificationDisplaySchemas])
def webhook_notification_display(db : Session = Depends(get_db)):

    data = db.query(Notification).all()

    return data


@router.get("/notification/display/{user_id}", response_model = list[NotificationDisplaySchemas])
def webhook_notification_display_by_userid(user_id : int, db: Session = Depends(get_db)):

    data = db.query(Notification).filter(Notification.user_id == user_id).all()

    if not data:
        raise HTTPException(status_code=404, detail="notification not found for the given user_id")

    return data


@router.delete("/notification/delete/{id}")
def webhook_notification_delete(id : int, db : Session = Depends(get_db)):

    data = db.query(Notification).filter(Notification.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="notification not found")
    
    db.delete(data)
    db.commit()
    db.refresh(data)

    return {
        "message" : "webhook notification deleted successfully"
    }

