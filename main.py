from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from pydantic_settings import BaseSettings
from functools import lru_cache
from routes.web import page_router 
# from . import config

from config import Settings
app = FastAPI()
app.include_router(page_router)


