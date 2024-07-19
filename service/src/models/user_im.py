from pydantic import BaseModel

class UserIm(BaseModel):
    id:int
    email:str
    role:str
    username:str
    password:str