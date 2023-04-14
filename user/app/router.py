from fastapi import APIRouter, Request , Form , status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from passlib.context import CryptContext
from . models import User
import typing
import passlib

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def flash(request: Request, message: typing.Any, category: str = "") -> None:
#     if "_messages" not in request.session:
#         request.session["_messages"] = []
#     request.session["_messages"].append({"message": message, "category": category})



# def get_flashed_messages(request: Request):
#     print(request.session)
#     return request.session.pop("_messages") if "_messages" in request.session else []


@router.get("/",response_class=HTMLResponse)
async def read_item(request : Request):
    return templates.TemplateResponse("signup.html", {"request" : request,})


@router.post("/registration/", response_class=HTMLResponse)
async def read_item(request : Request , email :str = Form(...),
                    name : str = Form(...),
                    phone : str = Form(...),
                    password : str = Form(...)):
    if await User.filter(email=email).exists():
        # flash(request , "Email already exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    
    elif await User.filter(phone=phone).exists():
        # flash(request , "Phone number already exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        
    else:
        await User.create(email=email,name=name,phone=phone,password=get_password_hash(password))
        # flash(request , "Successfully register")
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)    