from .BaseDataModel import BaseDataModle #type:ignore
from .db_schemes import project
from .enums.



class ProjectModel(BaseDataModle):
    def ___init__(self,db_client:object):
        super().__init__(db_client=db_client)
