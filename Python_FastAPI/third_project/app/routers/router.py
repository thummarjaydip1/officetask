from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from databases.database import get_db
from models.model import Person
from schemas.schma import PersonSchema, PersonSchemaUpdate, PersonSchemaDisplay
import datetime
from fastapi.responses import Response

router = APIRouter()

@router.post("/person/add")
def add_person(
    person : PersonSchema,
    db : Session = Depends(get_db)
):
    new_person = Person(
        name = person.name,
        email = person.email,
        address = person.address,
        birth_date = person.birth_date
    )
    db.add(new_person)
    db.commit()

    return {
        "message" : "Person detail added successfully",
        "id" : new_person.id
    }


@router.get("/person/get")
def get_person(
    db : Session = Depends(get_db)
):
    persons = db.query(Person).all()
    data = []

    for person in persons:
        data.append({
            "id" : person.id,
            "name" : person.name,
            "email" : person.email,
            "address" : person.address,
            "birth_date": person.birth_date
        })

    return data


@router.get("/person/get/{id}")
def get_person_id(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Person).filter(Person.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Person record not found")

    return {
        "id" : data.id,
        "name" : data.name,
        "email" : data.email,
        "address" : data.address,
        "birth_date" : data.birth_date
    }


@router.put("/person/update_full/{id}")
def update_full_person(
    id : int,
    person : PersonSchema,
    db : Session = Depends(get_db)
):
    data = db.query(Person).filter(Person.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Person detail not found")

    data.name = person.name
    data.email = person.email
    data.address = person.address
    data.birth_date = person.birth_date
    db.commit()

    return {
        "message" : "person data updated successfully",
        "id" : data.id
    }


@router.patch("/person/update/{id}")
def update_person(
    id : int,
    person : PersonSchemaUpdate ,
    db : Session = Depends(get_db)
):
    data = db.query(Person).filter(Person.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Person record not found")

    if person.name:
        data.name = person.name

    if person.email:
        data.email = person.email

    if person.address:
        data.address = person.address

    if person.birth_date:
        data.birth_date = person.birth_date

    db.commit()

    return {
        "message" : "Person record update successfully",
        "id" : data.id
    }


@router.delete("/person/delete/{id}")
def delete_person(
    id : int, 
    db : Session = Depends(get_db)
):
    data = db.query(Person).filter(Person.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Person record not found")

    db.delete(data)
    db.commit()
    return {
        "message" : "Person record deleted successfully"
    }


@router.get("/person/age/{id}")
def get_age_person(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Person).filter(Person.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Person record not found")

    birth_date = data.birth_date

    today = datetime.datetime.today().date()    

    age_year = today.year - birth_date.year

    age_month =  12 * age_year + (today.month - birth_date.month)

    age_day = (today - birth_date).days

    return {
        "birth_date" : birth_date,
        "today_date" : today,
        "age_year" : age_year,
        "age_month": age_month,
        "age_day" : age_day
    }


@router.head("/person/{id}")
def check_person(
    id : int, 
    db : Session = Depends(get_db)
):
    data = db.query(Person).filter(Person.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Person record not found")

    return Response(status_code=200)


@router.get("/person/search", response_model=list[PersonSchemaDisplay])
def search_person(
    name : str = None,
    db : Session = Depends(get_db)
):
    data = db.query(Person)

    if name:
        data = data.filter(
            Person.name.contains(name)
        )

    return data.all()


@router.get("/person/filter", response_model=list[PersonSchemaDisplay])
def filter_person(
    name : str = None,
    address : str = None,
    db : Session = Depends(get_db)
):
    data = db.query(Person)

    if name:
        data = data.filter(Person.name == name)

    if address:
        data = data.filter(Person.address == address)

    return data.all()


@router.get("/person/pagination", response_model=list[PersonSchemaDisplay])
def person_pagination(
    page : int = 1,
    size : int = 2,
    db : Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(status_code=400, detail="psgr must be greater than zero")

    if size < 1:
        raise HTTPException(status_code=400, detail="size must be greter than zero")

    data = db.query(Person).offset((page - 1) * size).limit(size).all()

    return data