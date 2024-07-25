from models.grade_im import GradeHomeworkIM, UpdateGradeHomeworkIM
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


from db.db_grade import (
    create_grade,
    get_report,
    get_user_report,
    update_grade,
    get_grade_homework,
    create_statistics,
)
from fastapi import Depends, APIRouter, HTTPException, status, UploadFile, File

import jwt
import os

router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.get("/get/report/{report_id}", tags=["grade"])
async def get_specific_report(report_id: int):

    report = get_report(report_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )

    return report


@router.get("/get/user/report/{user_id}", tags=["grade"])
async def get_report_user(user_id: int):

    report = get_user_report(user_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )

    return report


@router.get("/get/grade/homework/{homework_id}", tags=["grade"])
async def get_grade_from_specific_homework(homework_id: int):

    grade = get_grade_homework(homework_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Homeworks are not found",
        )

    return grade


@router.post("/create/grade/{homework_id}", tags=["grade"])
async def create_grades(
    grade_im: GradeHomeworkIM,
    homework_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]
    if user_role == "teacher" or user_role == "admin":

        grade = create_grade(
            grade_im.grade, grade_im.report, homework_id, grade_im.user_id
        )

        if not grade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Homeworks are not found",
            )

        return grade


@router.post("/create/statistics/{class_id}", tags=["grade"])
def create_statistic(class_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]

    if user_role == "teacher" or user_role == "admin":

        statistics = create_statistics(class_id)
        if not statistics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="statistics are not found",
            )

        return statistics


@router.put("/put/grade/{grade_id}", tags=["grade"])
async def get_report_user(
    grade_id: int,
    grade_im: UpdateGradeHomeworkIM,
    token: Annotated[str, Depends(oauth2_scheme)],
):

    payload = jwt.decode(token, public_key, algorithms=["RS256"])
    user_role: str = payload["user_role"]

    if user_role == "teacher" or user_role == "admin":

        grade_im.id = grade_id

        grade = update_grade(
            grade_im.id, grade_im.grade, grade_im.report, grade_im.homework_id
        )
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Homeworks are not found",
            )

        return grade
