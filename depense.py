from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from tools import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token=token)