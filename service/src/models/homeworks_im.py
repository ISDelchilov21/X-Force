from pydantic import BaseModel
from typing import Optional

class HomeworkIM(BaseModel):
    title:str
    type_homework:str
    info:str
    criteria:str
    status:str
    class_id:int

class SubmitHomeworkIM(BaseModel):
    text:str
    user_id:str

class HomeworkAttachmentIM(BaseModel):
    homework_id:int
    user_id:int
