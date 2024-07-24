from pydantic import BaseModel
from typing import Optional

class HomeworkIM(BaseModel):
    id:int
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
    id:int
    homework_id:str
    user_id:str
