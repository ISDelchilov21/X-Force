from pydantic import BaseModel

class LogoutIm(BaseModel):
    username:str
    password:str