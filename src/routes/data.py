from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController,ProcessController
from helpers.config import get_settings,Settings
from models import ResponseSignal
import logging
import os
import aiofiles 
from .schemes.data import ProccessRequest
from models.ProjectModel import ProjectModel
from models.DataChunkModel import DataChunkModel
from models.db_schemes import DataChunk




logger=logging.getLogger('uvicorn.error')
data_router=APIRouter(prefix="/data/v1",
                      tags=["api_v1","data"],
                      )

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id:str,file:UploadFile,app_settings:Settings = Depends(get_settings)):
    project_model=await ProjectModel.create_instance(
       db_client=request.app.db_client
    )
    project=await project_model.get_or_create_project(project_id=project_id)
    
    data_controller = DataController()

    is_valid,response_signal= data_controller.ValidateType(file=file)
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
                "file_id":file_id,
                }
        )
     


    return {"opreation done":response_signal,
            "file_id":file_id
            }



@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,proccess_request:ProccessRequest):
   
   file_id=proccess_request.file_id
   chunk_size=proccess_request.chunk_size
   overlap_size=proccess_request.overlap_size
   do_reset=proccess_request.do_reset

   project_model= await ProjectModel.create_instance(
       db_client=request.app.db_client
    )
   project=await project_model.get_or_create_project(project_id=project_id)
   
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

   file_chunks_records=[
      DataChunk(
         chunk_text=chunk.page_content,
         chunk_metadata=chunk.metadata,
         chunk_order=i+1,
         chunk_project_id=project.id
         )
      for i, chunk in enumerate(file_chunks)

   ]

   chunk_model= await DataChunkModel.create_instance(db_client=request.app.db_client)
   if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

   no_record= await chunk_model.insert_many_chunks(chunks=file_chunks_records)

   return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_record
        }
    )  
        
    
        
    
           
       

    