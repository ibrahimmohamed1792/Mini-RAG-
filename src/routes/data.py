from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from controllers import DataController
from helpers.config import get_settings,Settings
import os

data_router=APIRouter(prefix="/data/v1",
                      tags=["api_v1","data"],
                      )

@data_router.post("/upload/{project_id}")
def upload_data(project_id:str,file:UploadFile,app_settings:Settings = Depends(get_settings)):
    data_controller = DataController()

    is_valid,response_signal=data_controller.ValidateType(file=file)
    if not is_valid:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"opreation done":response_signal}
    )
    
    return {"opreation done":response_signal}