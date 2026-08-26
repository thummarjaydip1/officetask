from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from databases.database import get_db
from models.model import *

router = APIRouter(
    prefix="/categories",
    tags=["Category"]
)

@router.post("/add")
def add_category(
    name : str = Form(...),
    db : Session = Depends(get_db)
):
    new_category = Category(
        name=name
    )
    db.add(new_category)
    db.commit()

    return {
        "message" : "Category Added Successfully",
        "category_id" : new_category.id,
        "category_name" : new_category.name
    }


@router.get("/list")
def list_category(
    db : Session = Depends(get_db)
):
    categories = db.query(Category).all()
    data = []

    for i in categories:
        data.append({
            "id" : i.id,
            "name" : i.name
        })

    return data


@router.put('/update/{id}')
def update_category(
    id : int,
    name : str = Form(None),
    db : Session = Depends(get_db)
):
    data = db.query(Category).filter(Category.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Record not found")

    data.name = name
    db.commit()

    return {
        "message" : "Categoru updated successfully",
        "category_id" : data.id,
        "category_name" : data.name
    }


@router.delete("/delete/{id}")
def delete_category(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Category).filter(Category.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Reocrd not found")

    db.delete(data)
    db.commit()
    return {
        "message" : "data deleted successfully"
    }