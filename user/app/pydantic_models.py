from pydantic import BaseModel

class Person(BaseModel):
    email:str
    name:str
    phone:int
    password:str
    
    
class Loginuser(BaseModel):
    email : str
    password : str
        
class Token(BaseModel):
    access_token : str
    token_type : str = 'bearer'
    
class Onedata(BaseModel) :
    id : int
    
               
class Delete(BaseModel) :
    id : int
    
    
class Update(BaseModel):
    id : int
    email:str
    name:str
    phone:int
    password : str               