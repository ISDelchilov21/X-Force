from models.grade_im import GradeHomeworkIM, UpdateGradeHomeworkIM
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from langchain_core.prompts import PromptTemplate


from db.db_grade import (
    create_grade,
    get_report,
    get_user_report,
    update_grade,
    get_grade_homework,
    create_statistics,
)
from fastapi import Depends, APIRouter, HTTPException, status, UploadFile, File, Form

import jwt
import os

import models.gpt as gpt


router = APIRouter()

public_key = "\n".join(os.getenv("RSA_PUBLIC_KEY").split("<end>"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/ai", tags=["ai"])
async def generate_response(subject: str = Form(...), content: str = Form(...)):
    prompt_grading = PromptTemplate(
        template="Analyze closely the student's homework and give a grade with feedback based on the description. Follow closely the task given if there is one. If the task is empty give an overall feedback and grade\n{format_instructions}\n task: {task} \n homework: {content}\n",
        input_variables=[subject, content],
        partial_variables={"format_instructions": gpt.parser.get_format_instructions()},
    )

    prompt_plagiasm = PromptTemplate(
        template="Analyze closely the studen's homework word relations and text structure to determine if AI is used during creation of the homework. Take into account only answers if Question/Answer template is detected \n{format_instructions}\n{content}\n",
        input_variables=["content"],
        partial_variables={"format_instructions": gpt.parser.get_format_instructions()},
    )

    chain = gpt.generate_chain(prompt_grading, gpt.model, gpt.parser)
    p_chain = gpt.generate_chain(prompt_plagiasm, gpt.model, gpt.parser)

    result_plagiarism = p_chain.invoke({"content": content})
    result_grading = chain.invoke({"task": subject, "content": content})

    return result_plagiarism, result_grading
