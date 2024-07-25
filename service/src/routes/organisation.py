from models.organisations_im import (
    OrganisationIM,
    OrganisationGetIM,
    bridgeOrganisationUserIM,
    OrganisationJoinIM,
)
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from db.db_organisations import (
    create_org,
    get_org_by_name,
    get_org_by_code,
    add_user_to_organisation,
)
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
    return "".join(random.choice(charset) for _ in range(lenght))


@router.get("/get/organisation", tags=["org"])
async def get_organisation(org_im: OrganisationGetIM):
    org = get_org_by_name(org_im.name)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation is not found",
        )
    return org


@router.post("/organisation/create", tags=["org"])
async def create_orgasnisation(
    org_im: OrganisationIM, token: Annotated[str, Depends(oauth2_scheme)]
):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])

    user_id: int = payload["user_id"]
    user_role: str = payload["user_role"]
    if user_role == "admin":
        org_im.entry_code = generate_code(6)
        org_im.owner_id = user_id
        org_im.role = user_role

        org = create_org(org_im.name, org_im.entry_code, org_im.owner_id, org_im.role)

        if not org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organisation already exists",
            )


@router.post("/organisation/join", tags=["org"])
async def join_organisation(
    org_join_im: OrganisationJoinIM, token: Annotated[str, Depends(oauth2_scheme)]
):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    id: int = payload["user_id"]
    user_role: str = payload["user_role"]

    get_org = get_org_by_code(org_join_im.code)

    if not get_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation is not found",
        )

    org_im = bridgeOrganisationUserIM(
        user_id=id, user_role=user_role, org_id=get_org["id"], org_name=get_org["name"]
    )

    print(f"User ID:{org_im.user_id} Organisation ID: {org_im.org_id} ")
    org = add_user_to_organisation(
        org_im.user_id, org_im.user_role, org_im.org_id, org_im.org_name
    )

    return org
