from .providers import QdrantDBProvider
from VectorDBEnums import VectorDBEnums
class VectorDBProviderFactory():
    def __init(self,config:str):
        self.config=config


    def create(self,provider_name:str):
        if provider_name == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDBProvider(db_path=db_path,
                                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD)
        
        return None