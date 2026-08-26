from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from databases.database import get_db
from schemas.schema import StudentSchema, StudentDisplay
from models.model import Student

router = APIRouter(
    prefix="/students",
    tags=["Student"]
)

@router.post("/add")
def add_student(
    student : StudentSchema,
    db : Session = Depends(get_db)
): 
    new_student = Student(
        name = student.name,
        age = student.age,
        city = student.city
    )
    db.add(new_student)
    db.commit()

    return {
        "message" : "Student Record Added Successfully",
        "student_id" : new_student.id,
        "student_name" : new_student.name,
        "student_age" : new_student.age,
        "student_city" : new_student.city
    }


@router.get("/get")
def get_student(db : Session = Depends(get_db)):
    students = db.query(Student).all()
    data = []

    for student in students:
        data.append({
            "id" : student.id,
            "name" : student.name, 
            "age" : student.age,
            "city" : student.city
        })

    return data


@router.get("/get/{id}", response_model=StudentDisplay)
def get_one_student(
    id : int,
    db : Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == id).first()
    return student


@router.put("/update/{id}")
def update_student(
    id : int,
    student : StudentSchema,
    db : Session = Depends(get_db) 
):
    data = db.query(Student).filter(Student.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Student record not found")

    data.name = student.name
    data.age = student.age
    data.city = student.city
    db.commit()

    return {
        "mesage" : "Student Record Updated Successfully",
        "id" : data.id
    }


@router.delete("/delete/{id}")
def delete_record(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Student).filter(Student.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Student record not found")
    db.delete(data)
    db.commit()
    return {"message" : "Student Record Delete Successfully"}


@router.get("/search", response_model=list[StudentDisplay])
def search_student(
    name : str = None,
    db : Session = Depends(get_db)
):
    student = db.query(Student).all()

    if name:
        student = db.query(Student).filter(
            Student.name.contains(name)
        ).all()

    return student

@router.get("/filter", response_model=list[StudentDisplay])
def filter_student(
    name : str = None,
    age : int = None,
    city : str = None,
    db : Session = Depends(get_db)
):
    student = db.query(Student)

    if name:
        student = student.filter(Student.name == name)

    if age:
        student = student.filter(Student.age == age) 

    if city:
        student = student.filter(Student.city == city)

    return student.all()


@router.get("/pagination", response_model=list[StudentDisplay])
def pagination_student(
    page : int = 1,
    size : int = 3,
    db : Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than zero")

    if size < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than zero")

    student = db.query(Student).offset((page-1) * size).limit(size).all()

    return student