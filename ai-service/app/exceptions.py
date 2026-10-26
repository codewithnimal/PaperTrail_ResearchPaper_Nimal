"""
Custom exceptions and error handlers for the AI Service.
"""
from fastapi import HTTPException, status


class PdfProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class StorageAccessError(HTTPException):
    def __init__(self, detail: str = "Access to file storage failed or is not allowed"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class ServiceUnavailableError(HTTPException):
    def __init__(self, detail: str = "Service is temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )
