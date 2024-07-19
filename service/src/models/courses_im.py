from pydantic import BaseModel

class CourseIm(BaseModel):
    id:int
    owner_id:int
    org_id:int
    name:str
    code:str
    subject:str

class CourseScore(BaseModel):
    user_id:int
    course_id:int
    score:int
    position:int



    