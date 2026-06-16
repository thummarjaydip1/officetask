from fastapi import APIRouter
from schemas.feedback_schema import Feedback
from database.db import feed_conn, feed_cur

router = APIRouter()


@router.post("/send_feedback")
def send_feedback(feedback: Feedback):
    feed_cur.execute(
        "insert into feedback (name, message) values (?, ?)",
        (feedback.name, feedback.message),
    )
    feed_conn.commit()
    return {"message": "Feedback Send Successfully"}


@router.get("/display_feedback")
def display_feedback():
    feed_cur.execute("select * from feedback")
    data = feed_cur.fetchall()
    return data


@router.put("/update_feedback/{id}")
def update_feedback(id: int, feedback: Feedback):
    feed_cur.execute(
        "UPDATE feedback SET name = ?, message = ? WHERE id = ?",
        (feedback.name, feedback.message, id),
    )
    feed_conn.commit()
    return {"message": "Feedback Updated Successfully"}


@router.delete("/delete_feedback/{id}")
def delete_feedback(id: int):
    feed_cur.execute("delete from feedback where id=?", (id,))
    feed_conn.commit()
    return {"message": "Delete Feedback Successfully"}
