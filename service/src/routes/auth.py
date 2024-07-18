from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user_im import UserIm
from models.login_im import LoginIm
from models.token import Token
from db.db_user import auth_user, create_user

import jwt
import os
import datetime
import pytz

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
env = "\n".join(os.getenv("RSA_PRIVATE_KEY").split("<end>"))

@router.post("/login", tags=["auth"])
async def login(user_im: LoginIm):
    user = auth_user(user_im.username, user_im.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = jwt.encode({"iss": user["username"], "exp": datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(hours=3)}, env, algorithm="RS256") # type: ignore
    
    return Token(access_token=token, token_type="bearer")

@router.post("/token", tags=["auth"])
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = jwt.encode({"iss": user["username"], "exp": datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(hours=3)}, env, algorithm="RS256")
    
    return Token(access_token=token, token_type="bearer")

@router.post("/register", tags=["auth"])
async def register(user_im: UserIm):
    user = create_user(user_im.username, user_im.password,user_im.email, user_im.role)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )