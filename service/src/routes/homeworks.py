from models.homeworks_im import HomeworkIM, SubmitHomeworkIM, HomeworkAttachmentIM
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from azure.storage.blob.aio import BlobServiceClient

from db.db_homeworks import create_homework, get_homework_by_title, get_homework_by_id, add_homework_to_class, add_homework_to_user, get_homework_in_class,get_homeworks, get_homeworks_in_class, get_user_homework, delete_homework_by_id, delete_homework_by_title, update_homework, user_submit_homework, get_submited_homeworks, create_attachment, add_link_to_attachment, get_homeworks_in_class
from fastapi import Depends, APIRouter, HTTPException, status, UploadFile, File, Form
import uuid

import jwt
import os

router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))


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
async def create_homeworks(hm_im: HomeworkIM,class_id:int, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]
    
    if user_role == "teacher" or user_role == "admin":

        
        homework = create_homework(hm_im.title, hm_im.type_homework, hm_im.info, hm_im.criteria,class_id, hm_im.status)
        if not homework:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Homeworks are not found",
            )
        
    

        return homework
    
@router.post("/homework/create/attachment/{homework_id}", tags=["homeworks"])
async def create_attachments(homework_id:int, token: Annotated[str, Depends(oauth2_scheme)], body:str = Form(...), file:UploadFile = File(None),):
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]
    user_id: str = payload["user_id"]
    if user_role == "teacher" or user_role == "admin":

        attachment = create_attachment(homework_id, body, user_id)

        if file:
            _, extension = file.filename.split(".")
        
        print(f"\n\n{file.filename}\n\n")
        container_client = blob_service_client.get_container_client("files")
        
        try:
            if not await container_client.exists():
                await container_client.create_container()
                
            blob_client = container_client.get_blob_client(f"{uuid.uuid4()}.{extension}")
            
            await blob_client.upload_blob(await file.read(), blob_type="BlockBlob")
            add_link = add_link_to_attachment(blob_client.url, homework_id)
            
        except:
            raise HTTPException(status_code=500, detail="Could not upload file")
        
        return attachment, add_link


# @router.post("/class/create/homeworks/{class_id}", tags=["homeworks"])
# async def create_homeworks(hm_im: HomeworkIM, at_hm:HomeworkAttachmentIM,class_id:int, token: Annotated[str, Depends(oauth2_scheme)]):
#     payload = jwt.decode(token, public_key, algorithms=["RS256"])
#     user_role: str = payload["user_role"]
#     user_id: str = payload["user_id"]
#     if user_role == "teacher" or user_role == "admin":

        
#         homework = create_homework(hm_im.title, hm_im.type_homework, hm_im.info, hm_im.criteria,class_id, hm_im.status)
#         get_hm = get_homework_in_class(class_id)

#         at_hm.user_id = user_id


#         print(f" AND USER ID {homework} and the homework is{get_hm}")


@router.get("/get/homework/{homework_id}", tags=["homeworks"])
async def get_homework( homework_id:int):


    homework = get_homework_by_id(homework_id)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )
    

    return homework

@router.put("/put/homework/{homework_id}", tags="homework")
async def homework_update(homework_id:int, hm_im:HomeworkIM):
    
    homework = update_homework(hm_im.title, hm_im.type_homework, hm_im.info, hm_im.class_id, homework_id, hm_im.status)

    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )
    

    return homework


@router.delete("/delete/homework/{homework_id}", tags=["homeworks"])
async def delete_homework(homework_id:int):
    homework = delete_homework_by_id(homework_id)
    
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homework is not deleted",
        )


    return homework

@router.post("/submit/homework/{homework_id}",tags=["homeworks"])
async def submit_homework(homework_id:int, hm_im:SubmitHomeworkIM, token: Annotated[str, Depends(oauth2_scheme)] ):
    

    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]
    user_id: int = payload["user_id"]

    if user_role == "student":
        sumbit = user_submit_homework(hm_im.text, homework_id, user_id)
        if not sumbit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Homework is not deleted",
            )


        return sumbit
    
@router.get("/submited/homeworks/{user_id}")
async def get_submited_hm_user(token: Annotated[str, Depends(oauth2_scheme)] ):
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]
    user_id: int = payload["user_id"]

    if user_role == "student":
        sumbited = get_submited_homeworks(user_id)
        if not sumbited:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Homework is not deleted",
            )


        return sumbited