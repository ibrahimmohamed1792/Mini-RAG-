from enum import Enum


class ResponseSignal (Enum):
    FILE_VALIDATED_SUCCESS="file validated successfully"
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_SIZE_EXCEEDED="file size exceeded"
    FILE_UPLOAD_SUCCESS="file upload success"
    FILE_UPLOAD_FAILED="file upload fail"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing failed"
    NO_FILES_ERROR="no files found"
    NO_FILE_ERROR="no file with this id exists"
    PROJECT_NOT_FOUND_ERROR="this project is not here try looking somewhere else bro.."
    ERORR_WHILE_INSERTING="the vectordb is sleeping now comeback later"
    INSERT_INTO_VECTORDB_SUCCESS="ok got you ma boy here is how much you put us at work...happy now?!"
    NO_INFO_FOUND="no info found mate sorry"
    VECTORDB_COLLECTION_RETRIEVED="here you go man sleep on it and don't tell no one"
    SEARCH_FAILED_ERROR="we couldn't find whatever nonsense you've been looking for"
    SEARCH_SUCESS="here is the best matches for the nonsense you've been looking for no need to thank me now FUCK OFF!"