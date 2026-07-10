from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.model import Category
from schemas.category_schema import CategoryCreate, CategoryDisplay
from databases.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Category"]
)


@router.post("/add")
def add_category(
    category : CategoryCreate,
    db : Session = Depends(get_db)
):
    new_category = Category(
        name = category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "message" : "category added successfully",
        "id" : new_category.id,
        "name" : new_category.name
    }


@router.get("/get", response_model=list[CategoryDisplay])
def get_category(
    db : Session = Depends(get_db)
):
    data = db.query(Category).all()

    return data


@router.put("/update/{id}")
def update_category(
    id : int,
    category : CategoryCreate,
    db : Session = Depends(get_db)
):
    data = db.query(Category).filter(Category.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="category not found")
    
    data.name = category.name
    db.commit()
    db.refresh(data)

    return {
        "message" : "category updated successfully",
    }

@router.delete("/delete/{id}")
def delete_category(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Category).filter(Category.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="category not found")
    
    db.delete(data)
    db.commit()

    return {
        "message" : "category deleted successfully"
    }

@router.get("/search", response_model=list[CategoryDisplay])
def search_catogory(
    name : str = None,
    db : Session = Depends(get_db)
):
    data = db.query(Category).filter(
        Category.name.contains(name)
    ).all()


    return data