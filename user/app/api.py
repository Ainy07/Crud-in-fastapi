from fastapi import APIRouter, Request , Form , status
from fastapi.responses import HTMLResponse,RedirectResponse
from passlib.context import CryptContext
from . models import User
import typing
import passlib
from fastapi_login import LoginManager
from .pydantic_models import Person , LoginPerson

SECRET = 'your-secret-key'

app = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token')
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/registration_api/")
async def registration(data:Person):
    if await User.exists(phone = data.phone):
        return {"status":False,"message":"phone number already exists"}
    elif await User.exists(email = data.email):
        return {"status":False,"message":"email already exists"}
    else:
        user_obj = await User.create(email=data.email , name=data.name , phone=data.phone,
                                     password=get_password_hash(data.password))
        
        return user_obj
    
    
@manager.user_loader()
def load_user(email : str):
    user = User.get(email=email)
    return user
        
        
@router.post('/auth/token/login/')    
def login(data : 0Auth2PaswwordRequestForm = Depends()):
    email = data.username
    password = data.password
    
    user = load_user(email)
    if not user:
        raise InvalidCredentailsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token , 'token_type':'bearer'}

        