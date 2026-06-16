from fastapi import APIRouter
from schemas.contact_schema import Contact
from database.db import con_conn, con_cur

router = APIRouter()


@router.post("/send_contact")
def send_contact(contact: Contact):
    con_cur.execute(
        "insert into contact (name, age, email, city) values (?, ?, ?, ?)",
        (contact.name, contact.age, contact.email, contact.city),
    )
    con_conn.commit()
    return {"message": "Contact send Successfully"}


@router.get("/display_contact")
def display_contact():
    con_cur.execute("select * from contact")
    data = con_cur.fetchall()
    return data


@router.put("/update_contact/{id}")
def update_contcat(id: int, contact: Contact):
    con_cur.execute(
        "UPDATE contact SET name = ?, age = ?, email = ?, city = ? where id = ?",
        (contact.name, contact.age, contact.email, contact.city, id),
    )
    con_conn.commit()
    return {"message": "Contact Updated Successfully"}


@router.delete("/delete_contact/{id}")
def delete_contact(id: int):
    con_cur.execute("DELETE FROM contact WHERE id = ?", (id,))
    con_conn.commit()
    return {"message": "Contact Delete Successfully"}
