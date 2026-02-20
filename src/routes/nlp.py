from fastapi import FastAPI,APIRouter,Request,status
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseSignal 
from models.DataChunkModel import DataChunkModel
from models.ProjectModel import ProjectModel
from controllers.NLPController import NLPController
from .schemes.nlp import Push_request,Search_request
import json

import logging

logger = logging.getLogger('uvicorn.error')


nlp_router=APIRouter(
    prefix="/data/nlp/v1",
         tags=["api_v1","nlp"],
         )

@nlp_router.post("/push/{project_id}")
async def push_index(self,request:Request,push_requset:Push_request,project_id:str):
    project_model=await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_or_create_project(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
            }
        )

    data_chunk=await DataChunkModel.create_instance(db_client=request.app.db_client)

    NLP=NLPController(embedding_client=request.app.embedding_client,
                      generation_client=request.app.generation_client,
                      vectordb_client=request.app.vectordb_client,
                      template_parser=request.app.template_parser)
    



    has_records=True
    page_no=0
    inserted_items=0
    idx=0


    while has_records:
        page_chunks=await data_chunk.get_project_chunks(project_id=project.id,page_no=page_no)
        if page_chunks or len(page_chunks):
            page_no+=1
        if not page_chunks or len(page_chunks)==0 :
            has_records=False
            break


        chunks_ids =  list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted=NLP.push_into_vectordb(
            project=project,
            chunks=page_chunks,
            do_reset=push_requset.do_reset
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.ERORR_WHILE_INSERTING.value
                }
            )
        
        inserted_items+=len(page_chunks)
        if is_inserted:
             return JSONResponse(
        content={
            "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
            "inserted_items_count": inserted_items
        }
    )
        

@nlp_router.get("/get_info/{project_id}")
async def get_info(self,request:Request,project_id:str):

        project_model=await ProjectModel.create_instance(db_client=request.app.db_client)

        project = await project_model.get_or_create_project(
            project_id=project_id
        )

        if not project:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
                }
            )
        
        NLP=NLPController(embedding_client=request.app.embedding_client,
                      generation_client=request.app.generation_client,
                      vectordb_client=request.app.vectordb_client,
                      template_parser=request.app.template_parser)
        
        collection_info=NLP.get_collection_info(project)


        if not project:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.NO_INFO_FOUND.value
                }
            )
        
        return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info
        }
    )


@nlp_router.post("/search/{project_id}")
async def search_index(self,request:Request,search_request:Search_request,project_id:str):
     

        project_model=await ProjectModel.create_instance(db_client=request.app.db_client)

        project = await project_model.get_or_create_project(
            project_id=project_id
        )

        if not project:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
                }
            )
        

        NLP=NLPController(embedding_client=request.app.embedding_client,
                      generation_client=request.app.generation_client,
                      vectordb_client=request.app.vectordb_client,
                      template_parser=request.app.template_parser,)
        
        results=NLP.search_index(project=project,text=search_request.text,limit=search_request.limit)

        if not results:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.SEARCH_FAILED_ERROR.value
                }
            )
        

        if results:
             return JSONResponse(
        content={
            "signal": ResponseSignal.SEARCH_SUCESS.value,
            "results": json.loads(
            json.dumps(results, default=lambda x: x.__dict__)
        )
        }
    )
        

        
@nlp_router.post("/answer/{project_id}")
async def answer_rag(self,request:Request,search_request:Search_request,project_id:str):
        project_model = await ProjectModel.create_instance(
            db_client=request.app.db_client
        )

        project = await project_model.get_or_create_project(
            project_id=project_id
        )

        nlp = NLPController(
            vectordb_client=request.app.vectordb_client,
            generation_client=request.app.generation_client,
            embedding_client=request.app.embedding_client,
            template_parser=request.app.template_parser,
        )

        answer, full_prompt, chat_history= nlp.answer_rag(project=project,query=search_request.text,limit=search_request.limit)

        if not answer:
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "signal": ResponseSignal.RAG_ANSWER_ERROR.value
                    }
            )
    
        return JSONResponse(
            content={
                "signal": ResponseSignal.RAG_ANSWER_SUCCESS.value,
                "answer": answer,
                "full_prompt": full_prompt,
                "chat_history": chat_history
            }
        )


