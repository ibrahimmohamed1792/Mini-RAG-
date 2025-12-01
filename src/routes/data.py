from fastapi import FastAPI,APIRouter,Depends,UploadFile
from controllers import DataController
from helpers.config import get_settings,Settings
import os

data_router=APIRouter(prefix="/data/v1",
                      tags=["api_v1","data"],
                      )

@data_router.post("/upload/{project_id}")
def upload_data(project_id:str,file:UploadFile,app_settings:Settings = Depends(get_settings)):
    data_controller = DataController()

    is_valid=data_controller.ValidateType(file=file)

    return is_valid