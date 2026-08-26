from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from jose import jwt
from models.model import *
from databases.database import get_db
from auth import create_token, get_refresh_token, get_user, verify_password, SECRET_KEY, ALGORITHM


router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post('/register')
def user_register(
    username : str= Form(...) ,
    password : str = Form(...),
    email : str = Form(...),
    address : str = Form(...),
    db : Session = Depends(get_db)
):
    user_username = db.query(User).filter(User.username == username).first()
    if user_username:
        raise HTTPException(status_code=404, detail="username already exists")

    user_email = db.query(User).filter(User.email == email).first()
    if user_email:
        raise HTTPException(status_code=404, detail="email already exists")
    
    new_user = User(
        username=username,
        password=password,
        email=email,
        address=address
    )
    db.add(new_user)
    db.commit()
    return {
        "message" : "User Registration Successfully",
        "user_id" : new_user.id
    }


@router.post("/login")
def login_user(
    username : str = Form(...),
    password : str = Form(...),
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Username")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Password")

    access_token = create_token({"user_id" : user.id})

    refresh_token = get_refresh_token({"user_id" : user.id})

    return {
        "message" : "Login Successfully",
        "username" : user.username,
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }


@router.post("/refresh")
def refresh_token(
    token : str = Form(...)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id: 
            raise HTTPException(status_code=404, detail="Invalid User")

    except:
        raise HTTPException(status_code=404, detail="Login Again...")

    access_token = create_token({"user_id" : user_id})

    return{
        "access_token" : access_token
    }


@router.get("/list")
def user_list(
    db : Session = Depends(get_db)
):
    users = db.query(User).all()
    data = []

    for user in users:
        data.append({
            "id" : user.id,
            "username" : user.username,
            "password" : user.password,
            "email" : user.email,
            "address" : user.address
        })
    return data


@router.put("/update")
def update_user(
    id : int,
    username : str = Form(None),
    password : str = Form(None),
    email : str = Form(None),
    address : str = Form(None),
    db : Session = Depends(get_db)
):
    data = db.query(User).filter(User.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    data.username = username

    data.password = password

    data.email = email

    data.address = address

    db.commit()
    return {
        "message" : "User Update Successfully",
        "update_user_id" : data.id
    }


@router.delete("/delete")
def delete_user(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(User).filter(User.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not Found")

    db.delete(data)
    db.commit()
    return {
        "message" : "User Deleted Successfully  "
    }


@router.get("/profile")
def user_profile(
    user_id : int = Depends(get_user),
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    return {
        "id" : user.id,
        "username" : user.username,
        "password" : user.password,
        "email" : user.email,
        "address" : user.address
    }