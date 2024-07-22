from pydantic import BaseModel
from typing import Optional

class HomeworkIM(BaseModel):
    id:int
    title:str
    type_homework:str
    info:str
    class_id:int

class HomeworkAttachmentIM(BaseModel):
    id:int
    homework_id:str
    user_id:str
    text_info:str
    link:int