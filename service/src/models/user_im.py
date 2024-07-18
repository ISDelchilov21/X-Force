from pydantic import BaseModel

class UserIm(BaseModel):
    email:str
    role:str
    username:str
    password:str