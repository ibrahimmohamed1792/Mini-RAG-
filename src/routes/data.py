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
from models.AssetModel import AssetModel
from models.DataChunkModel import DataChunkModel
from models.db_schemes import DataChunk,Asset
from models import AssetTypeEnums



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
     
    asset_model=await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource=Asset(asset_project_id=project.id,
                         asset_type=AssetTypeEnums.FILE.value,
                         asset_name=file_id,
                         asset_size=os.path.getsize(file_path))
    
    asset_record=await asset_model.create_asset(asset=asset_resource)


    return {"opreation done":response_signal,
            "file_id":file_id
            }



@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProccessRequest):
    no_record = 0
    no_assets = 0

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    chunk_model = await DataChunkModel.create_instance(db_client=request.app.db_client)
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_or_create_project(project_id=project_id)
    project_file_ids = {}

    # --- 1. Fetching Assets ---
    if process_request.file_id:
        # Check if searching by name or ID. Usually, file_id from request is the asset_name
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )
        if asset_record:
            project_file_ids = {asset_record.id: asset_record.asset_name}
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"signal": ResponseSignal.NO_FILES_ERROR.value}
            )
    else:
        project_assets = await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnums.FILE.value
        )
        project_file_ids = {record.id: record.asset_name for record in project_assets}

    if not project_file_ids:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.NO_FILES_ERROR.value}
        )

    # --- 2. Reset Logic ---
    if process_request.do_reset == 1:
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    # --- 3. The Processing Loop ---
    processcontroller = ProcessController(project_id=project_id)

    for asset_id, file_id in project_file_ids.items():
        file_content = processcontroller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Can't find a source for the file: {file_id}")
            continue # Skip to next file, don't stop the whole process

        file_chunks = processcontroller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=process_request.chunk_size,
            overlap_size=process_request.overlap_size
        )

        if not file_chunks:
            logger.warning(f"No chunks generated for file: {file_id}")
            continue # Skip to next file

        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i + 1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]

        # INSERT INSIDE THE LOOP
        inserted_count = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_record += inserted_count
        no_assets += 1

    # --- 4. Final Response ---
    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_record,
            "no_assets_processed": no_assets
        }
    )