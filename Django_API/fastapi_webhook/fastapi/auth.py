from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "my_screate_key_with_jwt_project_with_fast_api"
ALGORITHM = "HS256"

oauth2_schemas = OAuth2PasswordBearer(tokenUrl="/users/login")

def verify_password(new_password: str, old_password: str):
    return new_password == old_password


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def create_refresh_token(data : dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days = 1)

    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_current_user(token : str = Depends(oauth2_schemas)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")
        
        return user_id
        
    except:
        raise HTTPException(status_code=401, detail="Login Agains...")