from pydantic import BaseModel


class GradeHomeworkIM(BaseModel):
    id: int
    grade: int
    report: str
    status: str
    homework_id: int
    user_id: int


class UpdateGradeHomeworkIM(BaseModel):
    id: int
    grade: int
    report: str
    homework_id: int
    status: str
