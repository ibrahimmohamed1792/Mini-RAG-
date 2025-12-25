from .BaseDataModel import BaseDataModel 
from .db_schemes import Assets
from .enums.DataBaseEnums import DataBaseEnum



class ProjectModel(BaseDataModel):
    def __init__(self,db_client :object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]