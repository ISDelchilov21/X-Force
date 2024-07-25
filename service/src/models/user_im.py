from pydantic import BaseModel


class UserIM(BaseModel):
    id: int
    email: str
    role: str
    username: str
    password: str


class UserGetIM(BaseModel):
    id: int
