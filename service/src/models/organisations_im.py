from pydantic import BaseModel


class OrganisationIM(BaseModel):
    id: int
    name: str
    entry_code: str
    owner_id: int
    role: str


class OrganisationGetIM(BaseModel):
    name: str


class OrganisationJoinIM(BaseModel):
    code: str


class bridgeOrganisationUserIM(BaseModel):
    user_id: int
    user_role: str
    org_id: int
    org_name: str


class bridgeOrganisationCourseIM(BaseModel):
    course_id: int
    org_id: int
