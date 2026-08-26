from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from models.model import *
from databases.database import get_db
from auth import get_user

router = APIRouter(
    prefix="/companies",
    tags=["Company"]
)

@router.post("/add")
def add_companies(
    name : str = Form(...),
    owner_name : str = Form(...),
    db : Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.name == name).first()
    if company:
        raise HTTPException(status_code=404, detail="Company already exists")

    new_company = Company(
        name = name,
        owner_name = owner_name
    )
    db.add(new_company)
    db.commit()
    return {
        "message" : "Company added Successfully",
        "id" : new_company.id
    }


@router.get("/list")
def company_list(
    db : Session = Depends(get_db)
):
    company = db.query(Company).all()
    data = []

    for i in company:
        data.append({
            "id" : i.id,
            "name" : i.name,
            "owner_name" : i.owner_name
        })
    return data


@router.put("/update")
def update_company(
    id : int,
    name : str = Form(None),
    owner_name : str = Form(None),
    db : Session = Depends(get_db)
):
    data = db.query(Company).filter(Company.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Comapny does nnot exitsts")

    data.name = name
    data.owner_name = owner_name
    db.commit()
    return {
        "message" : "company updated successfully",
        "id" : data.id
    }


@router.delete("/delete")
def delete_company(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Company).filter(Company.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(data)
    db.commit()
    return {
        "message" : "Company delete Successfully"
    }

