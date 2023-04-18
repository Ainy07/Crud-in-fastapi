from pydantic import BaseModel

class Person(BaseModel):
    email:str
    name:str
    phone:int
    password:str
    
    
class LoginPerson(BaseModel):
    email = str
    password = str    