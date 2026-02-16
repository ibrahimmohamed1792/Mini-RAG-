from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController
class VectorDBProviderFactory():
    def __init__(self,config:str):
        self.config=config


    def create(self,provider_name:str):
        if provider_name == VectorDBEnums.QDRANT.value:
            base_controller=BaseController()
            db_path =base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            

            return QdrantDBProvider(db_path=db_path,
                                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD)
        
        return None