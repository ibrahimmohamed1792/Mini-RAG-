from enum import Enum


class ResponseSignal (Enum):
    FILE_VALIDATED_SUCCESS="file validated successfully"
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_SIZE_EXCEEDED="file size exceeded"
    FILE_UPLOAD_SUCCESS="file upload success"
    FILE_UPLOAD_FAILED="file upload fail"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"