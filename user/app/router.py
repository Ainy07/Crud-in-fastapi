from fastapi import APIRouter, Request , Form , status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from passlib.context import CryptContext
from . models import User
import typing
import passlib
from fastapi_login import LoginManager



SECRET = 'your-secret-key'
router = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token')
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@manager.user_loader()
def load_user(email: str):  
    user = fake_db.get(email)
    return user



#registration
@router.get("/",response_class=HTMLResponse)
async def read_item(request : Request):
    return templates.TemplateResponse("signup.html", {"request" : request,})



@router.post("/registration/", response_class=HTMLResponse)
async def read_item(request : Request , email :str = Form(...),
                    name : str = Form(...),
                    phone : str = Form(...),
                    password : str = Form(...)):
    if await User.filter(email=email).exists():
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    elif await User.filter(phone=phone).exists():
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        
    else:
        await User.create(email=email,name=name,phone=phone,password=get_password_hash(password))
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)    
    
    
# @router.post('/auth/token')    
# def login(data : 0Auth2PaswwordRequestForm = Depends()):
#     email = data.username
#     password = data.password
    
#     user = load_user(email)
#     if not user:
#         raise InvalidCredentailsException
#     elif password != user['password']:
#         raise InvalidCredentialsException
    
#     access_token = manager.create_access_token(
#         data=dict(sub=email)
#     )
#     return {'access_token': access_token , 'token_type':'bearer'}


#login
@router.get("/login/",response_class=HTMLResponse)
async def read_item(request : Request):
    return templates.TemplateResponse("login.html", {"request" : request,})



@manager.user_loader()
async def load_user(email : str):
    if await User.exists(email=email):
        user = await User.get(email=email)
        return user
    
    
@router.post('/loginuser/')
async def login(request: Request, email: str = Form(...),
                password: str = Form(...)):
    email = email
    user = await load_user(email)
    if not user:
        return {'USER NOT REGISTERED'}
    elif not verify_password(password, user.password):
        return {'PASSWORD IS WRONG'}
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    if "_messages" not in request.session:
        request.session['_messages'] = []
        new_dict = {"user_id": str(
            user.id), "email": email, "access_token": str(access_token)}
        request.session['_messages'].append(
            new_dict
        )
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)


@router.get("/table/", response_class=HTMLResponse)
async def read_item(request: Request):
    users = await User.all()
    return templates.TemplateResponse("table.html", {
        "request": request,
        "users": users
    })
    
    
@router.get("/update/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    user = await User.get(id=id)
    return templates.TemplateResponse("update.html", {
        "request": request,
        "user": user
    })



@router.post("/update_user/")
async def update(request: Request, id: int = Form(...),
                 name: str = Form(...),
                 email: str = Form(...),
                 phone: str = Form(...),
                 ):
    user = await User.get(id=id)
    await User.filter(id=id).update(email=email,
                                      name=name,
                                      phone=phone
                                      )
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)


@router.get("/delete/{id}", response_class=HTMLResponse)
async def delete(request: Request, id: int):
    person_all = await User.get(id=id).delete()
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)