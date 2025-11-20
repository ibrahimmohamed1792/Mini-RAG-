from fastapi import FastAPI,APIRouter
import os
base_router=APIRouter(
    prefix="/base/v1",
    tags=["/base/v1"]
)

@base_router.get("/")
def Welcome():
    APP_name=os.getenv("APP_NAME")
    APP_ver=os.getenv("APP_VERSION")
    return{
        "response":"working",
        "app_name":APP_name,
        "app_ver":APP_ver
    }