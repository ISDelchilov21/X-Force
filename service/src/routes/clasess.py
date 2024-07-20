from models.classes_im import ClassesIM, ClassGetIM, bridgeClassUserIM,ClassJoinIM
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer



from db.db_classes import create_class, get_class_by_name, get_class_by_code, add_user_to_class, add_class_to_organisation
from fastapi import Depends, APIRouter, HTTPException, status
import random
import string
import jwt
import os

router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def generate_code(lenght):
    charset = string.ascii_letters + string.digits
    return ''.join(random.choice(charset) for _ in range(lenght))


@router.post("/class/{org_id}/create", tags=["class"])
async def create_orgasnisation(class_im: ClassesIM, org_id:int, token: Annotated[str, Depends(oauth2_scheme)]):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_id: int = payload["user_id"]

    class_im.entry_code = generate_code(6)
    class_im.owner_id = user_id

    class_im.org_id = org_id



    classes = create_class(class_im.name, class_im.subject, class_im.entry_code, class_im.org_id,class_im.owner_id)
    if not classes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class already exists",
        )
    
  
    
@router.post("/class/join", tags=["class"])
async def join_class(class_join_im: ClassJoinIM, token: Annotated[str, Depends(oauth2_scheme)]):

   
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    id: int = payload["user_id"]
    user_role:str = payload["user_role"]

    get_class = get_class_by_code(class_join_im.code)

    if not get_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class is not found",
        )
    
    class_im = bridgeClassUserIM(user_id=id, user_role=user_role,class_id=get_class['id'], class_name=get_class['name'], class_subject=get_class['subject'])

    org = add_user_to_class(class_im.user_id, class_im.user_role ,class_im.class_id, class_im.class_name, class_im.class_subject)

    return org


@router.post("/get/class", tags=["class"])
async def get_class(class_im:ClassGetIM):
    classes = get_class_by_name(class_im.name)

    if not classes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation is not found",
        )
    return classes