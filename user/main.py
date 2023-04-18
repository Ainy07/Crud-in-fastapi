# from typing import Union
from fastapi import FastAPI
from app import router as UsersRoute
from app import api as UsersAPI
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()


app.include_router(UsersRoute.router)
app.include_router(UsersAPI.app,tags=["api"])


register_tortoise(
    app,
    db_url="postgres://postgres:ainy@127.0.0.1/crud-fastapi",
    modules={"models": ['app.models',]},
    generate_schemas=True,
    add_exception_handlers=True
)
