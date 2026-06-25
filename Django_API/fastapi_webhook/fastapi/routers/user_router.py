from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import User, Product, Order, Wishlist, Cart
from schemas.user_schema import DisplayUser   #RegisterUser, LoginUser, UpdateUser
from auth import verify_password, create_access_token, create_refresh_token, get_current_user
from jose import jwt

import os
import shutil

router = APIRouter(
    prefix = "/users",
    tags = ["User"]
)

SECRET_KEY = "my_screate_key_with_jwt_project_with_fast_api"
ALGORITHM = "HS256"

# http://127.0.0.1:8000/users/register
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


# http://127.0.0.1:8000/users/login
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
    
    access_token = create_access_token({"user_id" : user.id})

    refresh_token = create_refresh_token({"user_id" : user.id})

    return {
        "message" : "Login Successfully",
        "username" : user.username,
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }


# http://127.0.0.1:8000/users/refresh
@router.post("/refresh")
def refresh(
    refresh_token : str = Form(...)
):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid user")

    except:
        raise HTTPException(status_code=401, detail="Login Agains...")

    access_token = create_access_token({
        "user_id" : user_id
    })

    return {
        "access_token" : access_token
    }


# http://127.0.0.1:8000/users/display
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


# http://127.0.0.1:8000/users/details/{id}
@router.get("/details/{id}")
def user_details(
    request : Request,
    id : int,
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User does not exists")

    products = db.query(Product).filter(Product.user_id == user.id).all()

    product_details = []
    
    for product in products:
        product_details.append({
            "product_id" : product.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}"
        })

    wishlists = db.query(Wishlist).filter(Wishlist.user_id == user.id).all()

    wishlist_detail = []

    for wishlist in wishlists:
        wishlist_product = db.query(Product).filter(Product.id == wishlist.product_id).first()
        wishlist_detail.append({
            "wishlist_id" : wishlist.id,
            "product_name"  : wishlist_product.name,
            "product_price"  :wishlist_product.price,
            "product_image" : str(request.base_url) + f"media/product/{wishlist_product.image}"
        })

    carts = db.query(Cart).filter(Cart.user_id == user.id).all()

    cart_details = []

    for cart in carts:
        cart_product = db.query(Product).filter(Product.id == cart.product_id).first()
        cart_details.append({
            "cart_id" : cart.id,
            "product_name" : cart_product.name,
            "product_price" : cart_product.price,
            "product_image" : str(request.base_url) + f"media/product/{cart_product.image}",
            "quantity" : cart.quantity,
            "total_price" : cart.total
        })

    orders = db.query(Order).filter(Order.user_id == user.id).all()

    order_details = []

    for order in orders:
        order_product = db.query(Product).filter(Product.id == order.product_id).first()
        order_details.append({
            "order_id" : order.id, 
            "product_name" : order_product.name,
            "product_price" : order_product.price,
            "product_image" : str(request.base_url) + f"media/product/{order_product.image}",
            "quantity" : order.quantity,
            "total_price"  :order.total
        })

    return {
        "user_id" : user.id,
        "image" :  str(request.base_url) + f"media/user/{user.image}",
        "username" : user.username,
        "email" : user.email,
        "address" : user.address,
        "user_added_product" : product_details,
        "user_wishlist" : wishlist_detail,
        "user_cart" : cart_details,
        "user_place_order" : order_details,
    }


# http://127.0.0.1:8000/users/update/password
@router.post("/update/password")
def user_update_password(
    username : str = Form(...), 
    password : str = Form(...),
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Username Not Found Please Enter Correct Username")
    
    if password:
        user.password = password

    db.commit()

    return {
        "message" : "Password Updated Successfully",
        "username" : user.username,
        "password" : user.password
    }


# http://127.0.0.1:8000/users/update/{id}
@router.put("/update/{id}")
def user_update(
    id: int,
    username: str = Form(None),
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
    data.email = email
    data.address = address

    if image:
        data.image = filename

    db.commit()

    return {
        "message" : "User Update Successfully",
        "id" : data.id 
    }


# http://127.0.0.1:8000/users/delete/{id}
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


# http://127.0.0.1:8000/users/profile
@router.get("/profile")
def profile(
    request: Request,
    user_id : int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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


# http://127.0.0.1:8000/users/search
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


# http://127.0.0.1:8000/users/count
@router.get("/count")
def count_user(
    db : Session = Depends(get_db)
):
    total_users = db.query(User).count()

    return {
        "total_users" : total_users
    }