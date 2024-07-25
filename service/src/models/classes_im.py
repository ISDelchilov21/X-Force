from pydantic import BaseModel


class ClassesIM(BaseModel):
    id: int
    owner_id: int
    org_id: int
    name: str
    entry_code: str
    subject: str


class ClassGetIM(BaseModel):
    name: str


class ClassJoinIM(BaseModel):
    code: str


class bridgeClassUserIM(BaseModel):
    user_id: int
    user_role: str
    class_id: int
    class_name: str
    class_subject: str


class ClassesScoreIM(BaseModel):
    user_id: int
    course_id: int
    score: int
    position: int
