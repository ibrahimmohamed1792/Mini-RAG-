from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
class DataController(BaseController) :
    def __init__(self):
        self.scale=1048576 
        super().__init__()


   
    def ValidateType(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE*self.scale:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        else:
            return True ,ResponseSignal.FILE_VALIDATED_SUCCESS