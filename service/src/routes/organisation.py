from models.organisations_im import OrganisationIm, OrganisationGetIm
from models.user_im import UserIm
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from db.db_organisations import create_org, get_org_by_name, delete_organisation
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


@router.post("/organisation/create", tags=["org"])
async def create_orgasnisation(org_im: OrganisationIm, token: Annotated[str, Depends(oauth2_scheme)]):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])

    user_id: int = payload["user_id"]
    user_role:str = payload["user_role"]

    org_im.entry_code = generate_code(6)
    org_im.owner_id = user_id
    org_im.role = user_role

    org = create_org(org_im.name, org_im.entry_code, org_im.owner_id, org_im.role)
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation already exists",
        ) 
@router.post("/get/organisation", tags=["org"])
async def get_organisation(org_im:OrganisationGetIm):
    org = get_org_by_name(org_im.name)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation is not found",
        )
    return org

