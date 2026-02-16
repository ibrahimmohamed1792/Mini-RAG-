from .BaseController import BaseController 
from models.db_schemes import Project,DataChunk
from typing import List
from stores.llms.LLMEnums import DocumentTypeEnum
import json



class NLPController(BaseController):


    def __init__(self,embedding_client,generation_client,vectordb_client):
        super().__init__()

        self.embedding_client= embedding_client
        self.generation_client=generation_client
        self.vectordb_client=vectordb_client


    def create_collection_name(self,project_id:str):
        return f"collection{project_id}".strip()
    
    def get_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        
        collection_info=self.vectordb_client.get_collection_info(collection_name)
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def push_into_vectordb(self,project:Project,chunks: List[DataChunk],do_reset: bool=False):


        ##get the name
        collection_name=self.create_collection_name(project_id=project.project_id)
        ## handle the parts
        texts=[c.chunk_text for c in chunks]
        metadatas=[c.chunk_metadata for c in chunks]
        vectors=[
            self.embedding_client.embed_text(text,document_type=DocumentTypeEnum.DOCUMENT)

            for text in texts
        ]
        ##create collection
        
        _=self.vectordb_client.create_collection(collection_name= collection_name, 
                                embedding_size=self.embedding_client.embedding_model_dim ,
                                do_reset=do_reset)
        
        _=self.vectordb_client.insert_many(collection_name=collection_name, texts=texts, 
                          vectors=vectors, metadata = metadatas, 
                          record_ids= None, batch_size = 50)
        
        return True
       


    
    
    def search_index(self,project:Project,text:str,limit:int=5):
        collection_name=self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.search_by_vector(collection_name=collection_name,
                                                     source_file=None,
                                                     vector= self.embedding_client.embed_text(text,document_type=DocumentTypeEnum.QUERY.value),
                                                     limit=limit)





    


    
