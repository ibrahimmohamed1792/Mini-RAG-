from fastapi import FastAPI,APIRouter,Depends
from helpers.config import get_settings,Settings
import os
base_router=APIRouter(
    prefix="/base/v1",
    tags=["/base/v1"]
)

@base_router.get("/")
async def Welcome(app_settings =Depends(get_settings)):
    #app_settings=get_settings()
    APP_name=app_settings.APP_NAME
    APP_ver=app_settings.APP_VERSION
    return{
        "response":"working",
        "app_name":APP_name,
        "app_ver":APP_ver
    }