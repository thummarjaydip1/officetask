from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import CreateStudent,DispStudent,UpdateStudent
from models import Student

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

@router.post("/add")
def add_student(student: CreateStudent , db: Session = Depends(get_db)):
    new_students = Student(
        name = student.name,
        email = student.email,
        city = student.city
    )
    db.add(new_students)
    db.commit()
    db.refresh(new_students)

    return {"message" : "Student Added"}

@router.get("/display",response_model=list[DispStudent])
def display_student(db: Session = Depends(get_db)):
    data = db.query(Student).all()
    return data

@router.put("/update/{id}")
def update_student(id: int,student: UpdateStudent , db: Session = Depends(get_db)):
    data = db.query(Student).get(id)
    if not data:
        return {"message":"Student not Found"}
    data.name = student.name
    data.email = student.email
    data.city = student.city
    db.commit()
    return {
        "message":"Student Data Updated Successfully",
        "Updated Student ID" : data.id,
        "Updated Student Name" : data.name,
        "Update Student Email" : data.email,
        "Update Student City" : data.city
    }

@router.delete("/delete/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    data = db.query(Student).get(id)

    if not data:
        return {"message" : "Id Does Not Exists"}
    
    db.delete(data)
    db.commit()
    return {"message" : "Student Data Delete Successfully"}


@router.get("/search", response_model=list[DispStudent])
def search_student(id: int = None, name: str = None, city: str = None, db: Session = Depends(get_db)):
    data = db.query(Student)
    if id:
        data = data.filter(Student.id.contains(id))
    if name:
        data = data.filter(Student.name.contains(name))
    if city:
        data = data.filter(Student.city.contains(city))
    return data.all()

@router.get("/count")
def count_student(db: Session = Depends(get_db)):
    data = db.query(Student).count()
    return {"total Student" : data}

