from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from schemas.user_schema  import CreateUser, LoginUser, UpdateUser
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/register")
def register(user: CreateUser):
    if User.objects.filter(username = user.username).exists():
        return {"error":"User already Exists....."}
    
    new_user = User.objects.create_user(
        username = user.username,
        password = user.password,
        email = user.email
    )
    return {
        "msg":"Register Successfully",
        "User id": new_user.id,
        "Username" : new_user.username
    }


@router.post('/login')
def login(user : LoginUser):
    if not User.objects.filter(username = user.username).exists():
        return {"error" : "user name not exists"}
    auth_user = authenticate(username = user.username , password = user.password)
    return {
        "msg" : "Login Successfully",
        "username" : auth_user.username
    }

@router.get('/get_user')
def get_user():
    users = User.objects.all()
    data = []
    for user in users:
        data.append({
            "id" : user.id,
            "username" : user.username,
            "password" : user.password,
            "email" : user.email
        })
    return data

@router.put("/update_user/{id}")
def update_user(id : int, user : UpdateUser):
    try:
        data = User.objects.get(id = id)
    except User.DoesNotExist:
        return HTTPException(status_code=404, detail="User id does not exists")
    if user.username:
        data.username = user.username
    if user.password:
        data.set_password(user.password)
    if user.email:
        data.email = user.email
    data.save()
    return {
        "msg" : "User Updated Successfully",
        "username" : data.username,
        "password" : data.password,
        "email" : data.email
    }

@router.delete("/delete_user/{id}")
def delete_user(id : int):
    user = User.objects.get(id=id)
    user.delete()
    return {"msg":"Usre Record Delete Successfully"}

