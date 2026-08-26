from jose import jwt 
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

SECRET_KEY = "auth_123_pro_456_secure_789"
ALGORITHM = "HS256"

outh2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_password(new_password, old_password):
    return new_password == old_password


def create_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=25)

    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_refresh_token(data : dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=1)

    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_user(
    token : str = Depends(outh2_schema)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=404, detail="Invalid User")

        return user_id

    except:
        raise HTTPException(status_code=404, detail="Login Again...")