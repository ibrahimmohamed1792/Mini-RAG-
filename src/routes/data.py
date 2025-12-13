from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController,ProcessController
from helpers.config import get_settings,Settings
from models import ResponseSignal
import logging
import os
import aiofiles # type: ignore
from .schemes.data import ProccessRequest




logger=logging.getLogger('uvicorn.error')
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
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orignal_file_name=file.filename,
        project_id=project_id
    )


    try:
        async with aiofiles.open(file_path,"wb") as f:
          while chunk := await file.read(app_settings.FILE_DEFULT_CHUNK_SIZE) :
            await f.write(chunk)
    except Exception as e:
        logger.error(f"error while uploading {e}")  
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"opreation done":response_signal,
                "file_id":file_id}
        )
     


    return {"opreation done":response_signal,
            "file_id":file_id}



@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,proccess_request:ProccessRequest):
   
   file_id=proccess_request.file_id
   chunk_size=proccess_request.chunk_size
   overlap_size=proccess_request.overlap_size
   
   processcontroller=ProcessController(project_id=project_id)

   file_content=processcontroller.get_file_content(file_id=file_id)
   file_id=proccess_request.file_id
   chunk_size=proccess_request.chunk_size
   overlap_size=proccess_request.overlap_size
   
   processcontroller=ProcessController(project_id=project_id)

   file_content=processcontroller.get_file_content(file_id=file_id)
   file_chunks=processcontroller.process_file_content(file_content=file_content,file_id=file_id,
                                                      chunk_size=chunk_size,overlap_size=overlap_size)
   if file_chunks is None or len(file_chunks) == 0:
       return JSONResponse(
           status_code=status.HTTP_400_BAD_REQUEST,
           content={
               "signal": ResponseSignal.PROCESSING_FAILED.value
           }
       )

   return file_chunks
        
    
        
    
           
       

    