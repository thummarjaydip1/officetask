from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.model import User, Product, Order
from schemas.user_schema import DisplayUser   #RegisterUser, LoginUser, UpdateUser
from auth import verify_password, create_access_token
from jose import jwt

import os
import shutil

router = APIRouter(
    prefix = "/users",
    tags = ["User"]
) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# profile in use code
oauth2_schemas = OAuth2PasswordBearer(tokenUrl="/user/login")

SECREAT_KEY = "my_screate_key_with_jwt_project_with_fast_api"
ALGORITHM = "HS256"


@router.post("/register")
def user_register(
    request : Request,
    username : str = Form(...),
    password : str = Form(...),
    email : str = Form(...),
    address : str = Form(...),
    image: UploadFile = File(...),
    db : Session = Depends(get_db)
):
    duplicate_username = db.query(User).filter(User.username == username).first()
    
    duplicate_email = db.query(User).filter(User.email == email).first()

    if duplicate_username:
        raise HTTPException(status_code=400, detail="User name already exists")
    
    if duplicate_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    

    os.makedirs("media/user", exist_ok=True)
    filename = image.filename
    filepath = f"media/user/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_user = User(
        username = username,
        password = password,
        email = email,
        address = address,
        image = filename
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message" : "User Registration Successfully",
        "id" : new_user.id,
        "username" : new_user.username,
        "password" : new_user.password,
        "email" : new_user.email,
        "address" : new_user.address,
        "image" : str(request.base_url) + f"media/user/{new_user.image}"
    }


@router.post("/login")
def user_login(
    username : str = Form(...),
    password : str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException (status_code = 404, detail = "Invalid Username")

    if not verify_password(password, user.password):
        raise HTTPException(status_code = 404, detail = "Invalid Password")
    
    token = create_access_token({"user_id" : user.id})

    return {
        "message" : "Login Successfully",
        "username" : user.username,
        "access token": token
    }


@router.get("/display")
def user_display(request: Request, db : Session = Depends(get_db)):
    users = db.query(User).all()
    
    data = []

    for user in users:
        data.append({
            "id" : user.id,
            "username" : user.username,
            "password" : user.password,
            "email" : user.email,
            "address" : user.address,
            "image" : str(request.base_url) + f"media/user/{user.image}",
            "create_at" : user.create_at
        })

    return data


@router.get("/details/{id}")
def user_details(
    request : Request,
    id : int,
    db : Session = Depends(get_db)
):
    user = db.query(User).get(id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User does not exists")

    products = db.query(Product).filter(Product.user_id == user.id).all()

    product_details =[]
    
    for product in products:
        product_details.append({
            "Product_id" : product.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}"
        })

    orders = db.query(Order).filter(Order.user_id == user.id).all()

    order_details = []

    for order in orders:
        pro = db.query(Product).filter(Product.id == order.product_id).first()
        order_details.append({
            "order_id" : order.id, 
            "product_name" : pro.name,
            "product_price" : pro.price,
            "product_image" : str(request.base_url) + f"media/product/{pro.image}"
        })

    data = []

    if user:
        data.append({
            "user_id" : user.id,
            "image" :  str(request.base_url) + f"media/user/{user.image}",
            "username" : user.username,
            "password" : user.password,
            "email" : user.email,
            "address" : user.address,
            "user_added_product" : product_details,
            "user_place_order" : order_details
        })
    return data


@router.put("/update/{id}")
def user_update(
    id: int,
    username: str = Form(None),
    password : str = Form(None),
    email : str = Form(None),
    address : str = Form(None),
    image : UploadFile = File(None),
    db: Session = Depends(get_db)    
):
    data = db.query(User).get(id)

    if not data:
        raise HTTPException(status_code=404, detail="User does not exists")
    
    os.makedirs("/media/user", exist_ok=True)
    filename = image.filename
    filepath = f"media/user/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    data.username = username
    data.password = password
    data.email = email
    data.address = address

    if data.image:
        data.image = filename

    db.commit()

    return {
        "message" : "User Update Successfully",
        "id" : data.id 
    }


@router.delete("/delete/{id}")
def user_delete(id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="User does not exists")
    
    # user image automatically delete from delete user record
    image_path = f"media/user/{user.image}"
    if os.path.exists(image_path):
        os.remove(image_path)

    db.delete(user)
    db.commit()

    return {"message" : "User Deleted Successfully"}


@router.get("/profile")
def profile(
    request: Request,
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
 
        if not user_id:
            raise HTTPException(status_code=404,detail="Invalid Token")
        
    except:
        raise HTTPException(status_code=404, detail="Login Again")
    
    user = db.query(User).filter(User.id == user_id).first()
    data =[]
    
    if user:
        data.append({
            "id" : user.id,
            "username" : user.username,
            "password" : user.password,
            "email" : user.email,
            "address" : user.address,
            "image" : str(request.base_url) + f"media/user/{user.image}",
            "create_at" : user.create_at
        })

        return data


@router.get("/search")
def search_user(
    request: Request,
    username: str = None,
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(
        User.username.contains(username)
    ).all()

    if not users:
        raise HTTPException(status_code=404, detail="Username does not exists")

    data = []

    for user in users:
        data.append({
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "address": user.address,
            "image": str(request.base_url) + f"media/user/{user.image}",
            "create_at": user.create_at
        })

    return data
