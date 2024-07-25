from pydantic import BaseModel


class LoginIm(BaseModel):
    username: str
    password: str
