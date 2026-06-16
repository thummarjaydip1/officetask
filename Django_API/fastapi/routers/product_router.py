from fastapi import APIRouter, HTTPException, Depends, File, Form, UploadFile, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.model import Product, User
from jose import jwt

import os
import shutil

router = APIRouter(
    prefix = "/products",
    tags = ["Products"]
)

oauth2_schemas = OAuth2PasswordBearer(tokenUrl="users/login")

SECREATE_KEY = "my_screate_key_with_jwt_project_with_fast_api"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def product_add(
    request: Request,
    name: str = Form(...),
    price: int = Form(...),
    image: UploadFile = File(...),
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECREATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")
        
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

        return {
            "message" : "Product Added Successfully",
            "product_id" : new_product.id,
            "product_name" : new_product.name,
            "product_price" : new_product.price,
            "product_image" : str(request.base_url) + f"media/product/{new_product.image}"
        }

    except:
        raise HTTPException(status_code=400, detail="Please Login Again...")
    

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


@router.put("/update/{id}")
def product_update(
    id: int,
    name: str = Form(None),
    price: str = Form(None),
    image: UploadFile = File(None),
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECREATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")
        
        product = db.query(Product).get(id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not Found")
        
        os.makedirs("media/product/", exist_ok=True)
        filename = image.filename
        filepath = f"media/product/{filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        product.name = name
        product.price = price

        if filename:
            product.image = filename
        
        db.commit()
        db.refresh(product)

        return {
            "message" : "Product Update Successfully",
            "id" : product.id
        }

    except:
        raise HTTPException(status_code=400, detail="Please Login Again...")
    
    
@router.delete("/delete/{id}")
def product_delete(
    id: int,
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECREATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")

        product = db.query(Product).filter(Product.id == id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # product image automatically delete from product record delete
        image_path = f"media/product/{product.image}"
        if os.path.exists(image_path):
            os.remove(image_path)


        db.delete(product)
        db.commit()

        return {"message": "Product Delete Successfully"}

    except:
        raise HTTPException(status_code=400, detail="Please Login Agains...")
    

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

        user = db.query(User).filter().first()

        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "username" : user.username
        })

    return data