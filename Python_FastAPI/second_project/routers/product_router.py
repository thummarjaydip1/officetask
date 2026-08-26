from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, Request
from sqlalchemy.orm import Session 
from databases.database import get_db
from models.model import *
import os
import shutil

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

@router.post("/add")
def add_product(
    name : str = Form(...),
    price : int = Form(...),
    image : UploadFile = File(...),
    category_id : int = Form(...),
    db : Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    os.makedirs("media/products", exist_ok=True)
    filename = image.filename
    filepath = f"media/products/{filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_product = Product(
        name = name,
        price = price,
        image = filename,
        category_id = category.id
    )
    db.add(new_product)
    db.commit()

    return {
        "message" : "Product Added Successfully",
        "name" : new_product.name,
        "price" : new_product.price
    }


@router.get("/list")
def list_product(
    request : Request,
    db : Session = Depends(get_db)
):
    products = db.query(Product).all()
    data = []

    for product in products:
        category = db.query(Category).filter(Category.id == product.category_id).first()
        
        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "image" : str(request.base_url) + f"media/products/{product.image}",
            "category_name" : category.name
        })

    return data


@router.put("/update/{id}")
def update_product(
    id : int,
    name : str = Form(None),
    price : int = Form(None),
    image : UploadFile = File(None),
    category_id : int = Form(None),
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='category not found')

    if image:
        os.makedirs("media/products", exist_ok=True)
        filename = image.filename
        filepath = f"media/products/{filename}"
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    product.name = name
    product.price = price
    product.image = filename
    product.category_id = category.id
    db.commit()

    return {
        "message" : 'Product updated successfully',
        "product_name" : product.name,
        "product_price" : product.price
    }


@router.delete("/delete/{id}")
def delete_product(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Product).filter(Product.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(data)
    db.commit()
    return {
        "message" : "Product Deleted Successfully"
    }