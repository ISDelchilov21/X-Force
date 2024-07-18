from pydantic import BaseModel

class OrganisationIm(BaseModel):
    name:str
    code:str
    owner_id:int
    role:str

class bridgeOrganisationUserIm(BaseModel):
    user_id:int
    org_id:int


class bridgeOrganisationCourseIm(BaseModel):
    course_id:int
    org_id:int
    