from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, Request
from sqlalchemy.orm import Session

from databases.database import get_db
from models.model import Student
# from schemas.schema import StudentSchema, StudentUpdate

import shutil
import os
router = APIRouter(
    prefix = "/students",
    tags = ["Student"]
)

@router.post("/add")
def add_student(
    image : UploadFile = File(...),
    name : str = Form(...),
    age : int = Form(...),
    email : str = Form(...),
    city : str = Form(...),
    db : Session = Depends(get_db)
):
    os.makedirs("media/student", exist_ok=True)
    filename = image.filename
    filepath = f"media/student/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_student = Student(
        image = filename,
        name = name,
        age = age,
        email = email,
        city = city
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return {
        "message" : "Student Added Successfully",
        "id" : new_student.id
    }


@router.get("/get")
def get_student(
    request : Request,
    db : Session = Depends(get_db)
):
    students = db.query(Student).all()

    data = []

    for student in students:
        data.append({
            "id" : student.id,
            "image" : str(request.base_url) + f"media/student/{student.image}",
            "name" : student.name,
            "age" : student.age,
            "email" : student.email,
            "city" : student.city
        })
    
    return data

@router.put("/update/{id}")
def update_student(
    id : int,
    image : UploadFile = File(None),
    name : str = Form(None),
    age : int = Form(None),
    email : str = Form(None),
    city : str = Form(None),
    db : Session = Depends(get_db)
):
    
    data = db.query(Student).filter(Student.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Student id not found")

    if image:
        os.makedirs("media/student", exist_ok=True)
        filename = image.filename
        filepath = f"media/student/{filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    if image:
        data.image = filename

    if name:
        data.name = name
        
    if age:
        data.age = age
        
    if email:
        data.email = email
        
    if city:
        data.city = city

    db.commit()
    db.refresh(data)

    return {
        "message" : "Student Record Updated Successfully",
        "updated record id" : data.id
    }


@router.delete("/delete")
def delete_student(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Student).filter(Student.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Student id not found")
    
    db.delete(data)
    db.commit()

    return {
        "message" : "Studetn Recod Deleted Successfully"
    }