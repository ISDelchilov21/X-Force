from pydantic import BaseModel

class OrganisationIm(BaseModel):
    id:int
    name:str
    entry_code:str
    owner_id:int
    role:str

class OrganisationGetIm(BaseModel):
    name:str


class bridgeOrganisationUserIm(BaseModel):
    user_id:int
    org_id:int


class bridgeOrganisationCourseIm(BaseModel):
    course_id:int
    org_id:int
    