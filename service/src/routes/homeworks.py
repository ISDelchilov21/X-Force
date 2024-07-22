from models.homeworks_im import HomeworkIM
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


from db.db_homeworks import create_homework, get_homework_by_title, get_homework_by_id, add_homework_to_class, add_homework_to_user, get_homeworks, get_homeworks_in_class, get_user_homework, delete_homework_by_id, delete_homework_by_title, update_homework
from fastapi import Depends, APIRouter, HTTPException, status, UploadFile, File
import uuid

import jwt
import os

router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")



@router.get("/get/homework/by/{homework_title}", tags=["homeworks"])
async def get_homework( homework_title:str):


    homework = get_homework_by_title(homework_title)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homework name is not found",
        )
    return homework


@router.get("/get/homework/{homework_id}", tags=["homeworks"])
def get_homework( homework_id:int):


    homework = get_homework_by_id(homework_id)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homework id is not found",
        )
    return homework

@router.get("/get/homework/class/{class_id}", tags=["homeworks"])
def get_homework( class_id:int):


    homework = get_homeworks_in_class(class_id)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homework id is not found",
        )
    return homework
@router.get("/get/homework/user/{user_id}", tags=["homeworks"])
def get_homework( user_id:int):


    homework = get_user_homework(user_id)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homework id is not found",
        )
    return homework

@router.get("get/homeworks",tags=["homeworks"])
def get_all_homeworks():
    homeworks = get_homeworks()
    if not homeworks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )
    return homeworks




@router.post("/class/create/homeworks/{class_id}", tags=["homeworks"])
async def create_homeworks(hm_im: HomeworkIM, class_id:int, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: int = payload["user_role"]
    if user_role == "teacher" or user_role == "admin":

        
        homework = create_homework(hm_im.title, hm_im.type_homework, hm_im.info, class_id)
        
        print(hm_im.id)

        if not homework:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Homeworks are not found",
            )
    

        return homework
    


@router.get("/get/homework/{homework_id}", tags=["homeworks"])
async def get_homework( homework_id:int):


    homework = get_homework_by_id(homework_id)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )
    

    return homework

router.put("/put/homework/{homework_id}", tags="homeworks")
async def homework_update(homework_id:int, hm_im:HomeworkIM):
    
    homework = update_homework(hm_im.title, hm_im.type_homework, hm_im.info, hm_im.class_id, homework_id)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )
    

    return homework


router.delete("/delete/homework/{homework_id}", tags=["homeworks"])
async def delete_homework(homework_id:int):
    homework = delete_homework_by_id(homework_id)
    
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homework is not deleted",
        )


    return homework