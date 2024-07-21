from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
import os
from typing import Annotated
import db.db_user
from models.user_im import UserIM, UserGetIM
from db.db_user import get_user_by_id, update_user, delete_user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))

@router.get("/get/user", tags=["users"])
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        username: str = payload["iss"]

        user = db.db_user.get_user_by_username(username)

        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

@router.get("/get/user/{user_id}", tags=["users"])
async def get_user( user_id:int):
    
    
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not found",
        )
    return user


@router.put("/put/user/{user_id}", tags=["users"])
async def user_update( user_id:int, user_im:UserIM):

    user_im.id = user_id

    user = update_user(user_im.email, user_im.role, user_im.username, user_im.password, user_im.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not found",
        )
    return user


@router.delete("/delete/user/{user_id}", tags=["users"])
async def user_delete( user_id:int, token: Annotated[str, Depends(oauth2_scheme)]):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])

    user_role:str = payload["user_role"]

    print(f"IS IT ADMIN:{user_role}")

    if user_role == "admin":

        user = delete_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not found",
            )
        return user