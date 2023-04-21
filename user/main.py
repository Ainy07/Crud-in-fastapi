# from typing import Union
from fastapi import FastAPI
from app import router as UsersRoute
from app import api as UsersAPI
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware

middleware = [
    Middleware(SessionMiddleware, secret_key='super-secret')
]

app = FastAPI(middleware=middleware)

app.include_router(UsersRoute.router)
app.include_router(UsersAPI.app,tags=["api"])


register_tortoise(
    app,
    db_url="postgres://postgres:ainy@127.0.0.1/crud-fastapi",
    modules={"models": ['app.models',]},
    generate_schemas=True,
    add_exception_handlers=True
)
