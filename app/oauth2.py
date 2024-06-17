from .import schemas
from .config import settings
from typing import Annotated
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, DecodeError, decode
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = settings.secret_key  # To Verify with backedn
ALGORITHM = settings.algorithm
EXPIRATION_TIME_OF_TOKEN = settings.expiration_time_of_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authntication/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes= EXPIRATION_TIME_OF_TOKEN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("username")
        email:str = payload.get("email")
        user_id:int = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, email=email, user_id=user_id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Session expired. Please log in again.",
                            headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise credentials_exception    
    except DecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could Not Validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could Not Validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)