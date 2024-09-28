from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from pydantic_settings import BaseSettings
from functools import lru_cache
from routes.web import page_router 
# from . import config

from config import Settings
app = FastAPI()
app.include_router(page_router)


@lru_cache
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.FEDEX_SECRET_KEY,
        "admin_email": settings.FEDEX_API_KEY,
        "items_per_user": settings.FEDEX_BASE_API_URL,
    }


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}