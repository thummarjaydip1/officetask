from fastapi import APIRouter, HTTPException, Depends, File, Form, UploadFile, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import Product, User
from auth import get_current_user

import requests
import os
import shutil

router = APIRouter(
    prefix = "/products",
    tags = ["Products"]
)


# http://127.0.0.1:8000/products/add
@router.post("/add")
def product_add(
    request: Request,
    name: str = Form(...),
    price: int = Form(...),
    image: UploadFile = File(...),
    user_id : int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    os.makedirs("media/product", exist_ok=True)
    filename = image.filename
    filepath = f"media/product/{filename}"

    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    new_product = Product(
        name = name,
        price = price,
        image = filename,
        user_id = user_id            
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    try:
        requests.post(
            "http://127.0.0.1:9000/webhook/notification/add",
            json = {
                "user_id" : user_id,
                "message" : "product added successfully"
            }
        )

    except Exception as e:
        print("webhook error:", e)

    return {
        "message" : "Product Added Successfully",
        "product_id" : new_product.id,
        "product_name" : new_product.name,
        "product_price" : new_product.price,
        "product_image" : str(request.base_url) + f"media/product/{new_product.image}"
    }
    

# http://127.0.0.1:8000/products/display
@router.get("/display")
def product_display(
    request: Request,
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()
    data = []

    for product in products:

        user = db.query(User).filter(User.id == product.user_id).first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "username" : user.username
        })
    
    return data


# http://127.0.0.1:8000/products/filter/display
@router.get("/filter/display")
def product_filter_display(
    request : Request,
    username : str = None,
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Username does not exists")
    
    products = db.query(Product).filter(
        Product.user_id == user.id
    ).all()

    data = []
    
    for product in products:

        users = db.query(User).filter(User.id == product.user_id).first()
        
        data.append({
            "id" : product.id,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "name" : product.name,
            "price" : product.price,
            "username" : users.username
        })

    return data


# http://127.0.0.1:8000/products/my-products
@router.get("/my-products")
def display_my_product(
    request : Request,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    products = db.query(Product).filter(Product.user_id == user_id).all()
        
    data = []

    for product in products:
            
        user = db.query(User).filter(User.id == product.user_id).first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "image"  : str(request.base_url) + f"media/product/{product.image}",
            "username" : user.username
        })

    return data


# http://127.0.0.1:8000/products/update/{id}
@router.put("/update/{id}")
def product_update(
    id : int,
    name : str = Form(None),
    price : str = Form(None),
    image : UploadFile = File(None),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    product = db.query(Product).get(id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not Found")
    
    if product.user_id != user_id:
        raise HTTPException(status_code=400, detail="you can update only own added product")
    
    os.makedirs("media/product/", exist_ok=True)
    filename = image.filename
    filepath = f"media/product/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    product.name = name
    product.price = price

    if image:
        product.image = filename

    db.commit()
    db.refresh(product)

    try:
        requests.post(
            "http://127.0.0.1:9000/webhook/notification/add",
            json = {
                "user_id" : user_id,
                "message" : "product updated successfully"
            }
        )

    except Exception as e:
        print("webhook error:", e)

    return {
        "message" : "Product Update Successfully",
        "id" : product.id
    }
    
    
# http://127.0.0.1:8000/products/delete/{id}
@router.delete("/delete/{id}")
def product_delete(
    id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.user_id != user_id:
        raise HTTPException(status_code=401, detail="You can delete only own added product")

    # product image automatically delete from product record delete
    image_path = f"media/product/{product.image}"
    if os.path.exists(image_path):
        os.remove(image_path)

    db.delete(product)
    db.commit()

    try:
        requests.post(
            "http://127.0.0.1:9000/webhook/notification/add",
            json = {
                "user_id" : user_id,
                "message" : "product deleted successfully"
            }
        )

    except Exception as e:
        print("webhook error:", e)

    return {"message": "Product Delete Successfully"}

    
# http://127.0.0.1:8000/products/search
@router.get("/search")
def search_product(
    request: Request,
    name: str = None,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.name.contains(name)
    ).all()

    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    data = []

    for product in products:

        user = db.query(User).filter(User.id == product.user_id).first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "username" : user.username
        })

    return data


# http://127.0.0.1:8000/products/count
@router.get("/count")
def count_product(
    db : Session = Depends(get_db)
):
    total_products = db.query(Product).count()

    return {
        "total_products" : total_products
    }