from models.themes_im import ThemesIM, ThemeGetIM, ThemesClasssIM
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from db.db_themes import create_themes, get_theme_by_title, get_theme_by_id
from fastapi import Depends, APIRouter, HTTPException, status

import jwt
import os

router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/theme/{class_id}/create", tags=["theme"])
async def create_theme(theme_im: ThemesIM, class_id:int, token: Annotated[str, Depends(oauth2_scheme)]):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_id: int = payload["user_id"]
    theme_im.owner_id = user_id
    theme_im.class_id = class_id



    theme = create_themes(theme_im.title, theme_im.unique_info, theme_im.class_id, theme_im.owner_id)
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class already exists",
        )


@router.post("/get/theme", tags=["theme"])
async def get_theme(theme_im:ThemeGetIM):
    theme = get_theme_by_title(theme_im.title)
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation is not found",
        )
    return theme