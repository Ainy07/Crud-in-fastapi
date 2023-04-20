from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from passlib.context import CryptContext
from . models import User
import typing
import passlib
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from .pydantic_models import Person, Loginuser, Token , Delete , Update , Onedata

SECRET = 'your-secret-key'

app = APIRouter()
manager = LoginManager(SECRET, token_url='/user_login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/registration_api/")
async def registration(data: Person):
    if await User.exists(phone=data.phone):
        return {"status": False, "message": "phone number already exists"}
    elif await User.exists(email=data.email):
        return {"status": False, "message": "email already exists"}
    else:
        user_obj = await User.create(email=data.email, name=data.name, phone=data.phone,
                                     password=get_password_hash(data.password))

        return user_obj


@manager.user_loader()
async def load_user(email: str):
    if await User.exists(email=email):
        user = await User.get(email=email)
        return user


@app.post('/login/')
async def login(data: Loginuser ):
    email = data.email
    user = await load_user(email)

    if not user:
        return JSONResponse({'status': False, 'message': 'User not registered '}, status_code=403)
    elif not verify_password(data.password, user.password):
        return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(
        data={'sub': dict({'id': jsonable_encoder(user.id)}), }
    )

    new_dict = jsonable_encoder(user)
    new_dict.update({'access_token': access_token})
    return Token(access_token=access_token, Token_type='bearer')


@app.get('/data/')
async def all_user():
    user = await User.all()
    return user

@app.post('/data_one/{id}')
async def one_data(data:Onedata):
    user = await User.get(id=data.id)
    return user



@app.delete("/delete_user/{id}")
async def delete(data:Delete):
    user_obj = await User.get(id = data.id).delete()
    return {"status":True , "message":"delete user"} 


@app.put("/update_user/{id}")
async def update(data:Update):
    if await User.exists(phone=data.phone):
        return {"status": False, "message": "phone number already exists"}
    elif await User.exists(email=data.email):
        return {"status": False, "message": "email already exists"}
    else:
        user_obj = await User.filter(id = data.id).update(email=data.email, name=data.name, phone=data.phone,
                                     password=get_password_hash(data.password))

        return {"status": True, "message": "update successfully"}