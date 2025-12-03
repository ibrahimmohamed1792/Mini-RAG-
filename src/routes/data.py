from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController
from helpers.config import get_settings,Settings
import os
import aiofiles

data_router=APIRouter(prefix="/data/v1",
                      tags=["api_v1","data"],
                      )

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings:Settings = Depends(get_settings)):
    data_controller = DataController()

    is_valid,response_signal=data_controller.ValidateType(file=file)
    if not is_valid:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"opreation done":response_signal}
    )
    project_dir_path=ProjectController().get_project_path(Project_id=project_id)
    file_path=os.path.join(project_dir_path,file.filename)

    async with aiofiles.open(file_path,"wb") as f:
        while chunk := await file.read(app_settings.FILE_DEFULT_CHUNK_SIZE) :
            await f.write(chunk)


    return {"opreation done":response_signal}



