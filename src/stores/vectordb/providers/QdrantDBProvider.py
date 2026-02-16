from qdrant_client import QdrantClient,models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List
import uuid

class QdrantDBProvider(VectorDBInterface):

    def __init__(self,db_path:str,distance_method:str):
        self.client=None
        self.db_path=db_path
        self.distance_method=distance_method

        if distance_method == DistanceMethodEnums.COSINE.value :
            self.distance_method = models.Distance.COSINE

        
        if distance_method == DistanceMethodEnums.DOT.value :
            self.distance_method = models.Distance.COSINE
        
        
        self.logger=logging.getLogger(__name__)
        

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        return None
    

    def is_collection_existed(self, collection_name: str) -> bool:
         if self.client.collection_exists(collection_name=collection_name):
             return True
         
         return False
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    

    def list_all_collections(self) -> List:
       return self.client.get_collections()
    
    def delete_collection(self, collection_name: str):
       if self.client.collection_exists(collection_name=collection_name):
        return self.client.delete_collection(collection_name=collection_name)
    

    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        if do_reset:
           _ = self.client.delete_collection(collection_name=collection_name)
           
           
        if not self.is_collection_existed(collection_name):
             _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )

             return True
        
        return False
    


    def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"can't insert into this collection it doesn't even exist idiot{collection_name}")
            return None
        
        try:
            _ = self.client.upload_points(
                collection_name=collection_name,
                points=[
                    models.Record(
                        id=record_id,
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting record: {e}")
            return False
        return True
        
    def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50):
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = [None] * len(texts)

        if record_ids is None:
           record_ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            b_ids = record_ids[i:batch_end]
            
            
            
            batch_records = []

            
                        
            
            for text, vector, meta,rid in zip(batch_texts, batch_vectors, batch_metadata,b_ids):
                
                final_id = rid if rid is not None else str(uuid.uuid4())
                record = models.Record(
                    id=final_id,
                    vector=vector,
                    payload={"text": text, "metadata": meta}
                )
                batch_records.append(record)

                try:
                    _ = self.client.upload_points(
                        collection_name=collection_name,
                        points=batch_records,
                    )
                except Exception as e:
                    self.logger.error(f"Error while inserting batch: {e}")
                    return False

        return True
        
    def search_by_vector(self, collection_name: str,source_file:str, vector: list, limit: int = 5):

        query_filter=None

        if source_file:
          
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source", # Path to the key in your payload
                        match=models.MatchValue(value=source_file)
                    )
                ]
            )

        return self.client.query_points(
            collection_name=collection_name,
            query=vector,
            query_filter=query_filter,
            limit=limit
        )
        

  
    

    
