from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from sqlalchemy.orm import Session

from models.model import Product, Category
from databases.database import get_db

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
    stock : int = Form(...),
    description : str = Form(...),
    image : UploadFile = File(...),
    category_name : str = Form(...),
    db : Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.name == category_name).first()

    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    
    os.makedirs("media/products", exist_ok=True)
    filename = image.filename
    filepath = f"media/products/{filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_product = Product(
        name = name,
        price = price,
        stock = stock,
        description = description,
        image = filename,
        category = category.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message" : "product added successfully"
    }


@router.get("/get")
def get_product(
    request : Request,
    db : Session = Depends(get_db)
):
    products = db.query(Product).all()

    data = []

    for product in products:
        
        category = db.query(Category).filter(Category.id == product.category).first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "stock" : product.stock,
            "description" : product.description,
            "image" : str(request.base_url) + f"media/products/{product.image}",
            "category" : category.name,
            "create_at" : product.create_at
        })

    return data


@router.put("update/{id}")
def update_product(
    id : int,
    name : str = Form(None),
    price : int = Form(None),
    stock : int = Form(None),
    description : str = Form(None),
    image : UploadFile = File(None),
    category_name : str = Form(None),
    db : Session = Depends(get_db)
):
    if category_name:
        category = db.query(Category).filter(Category.name == category_name).first()

        if not category:
            raise HTTPException(status_code=404, detail="category not found")
    
    data = db.query(Product).filter(Product.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="prodduct not found")
    
    if image:
        filename = image.filename
        filepath = f"media/products/{filename}"
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    if name:
        data.name = name
    if price:
        data.price = price
    if stock:
        data.stock = stock
    if description:
        data.description = description
    if image:
        data.image = filename
    if category_name:
        data.category = category.id
    
    db.commit()
    db.refresh(data)

    return {
        "message" : "product updated successfully"
    }



@router.delete("/delete/{id}")
def delete_product(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Product).filter(Product.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="product not found")
    
    db.delete(data)
    db.commit()

    return {
        "message" : "product deleted successfully"
    }


@router.get("/search")
def search_product(
    request : Request,
    name : str = None,
    db : Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.name.contains(name)
    ).all()

    data = []

    for product in products:
        
        category = db.query(Category).filter(Category.id == product.category).first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "stock" : product.stock,
            "description" : product.description,
            "image" : str(request.base_url) + f"media/products/{product.image}",
            "category" : category.name,
            "create_at" : product.create_at
        })

    return data


@router.get("/filter")
def filter_product_by_category(
    request : Request,
    category_name : str = None,
    db : Session = Depends(get_db)
):
    products = db.query(Product).all()

    if category_name:
        category = db.query(Category).filter(Category.name == category_name).first()

        if not category:
            raise HTTPException(status_code=404, detail="category not found")
        
        products = db.query(Product).filter(Product.category == category.id).all()

    data = []

    for product in products:
        
        category = db.query(Category).filter(Category.id == product.category).first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "stock" : product.stock,
            "description" : product.description,
            "image" : str(request.base_url) + f"media/products/{product.image}",
            "category" : category.name,
            "create_at" : product.create_at
        })

    return data

@router.options("/option")
def option_product(
    db : Session = Depends(get_db)
):
    products = db.query(Product).all()

    data = []

    for product in products:
        
        data.append(product.name)

    return data