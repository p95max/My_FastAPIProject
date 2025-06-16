from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from pytz import utc

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = 'FNFEFN884835HFUDVHD'

def create_access_token(data: dict):
    expire = datetime.now(tz=utc) + timedelta(minutes=30)
    data.update({"exp": expire})
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="JWT error")

def validate_password(password, hash_password):
    return pwd_context.verify(password, hash_password)

def hashed_password(password):
    return pwd_context.hash(password)


