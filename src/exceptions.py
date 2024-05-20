from fastapi import HTTPException

from fastapi import FastAPI
from starlette.responses import JSONResponse


class ObjectNotFound(HTTPException):
    def __init__(self, status_code: int = 404, detail: str = "Object not found"):
        super().__init__(status_code, detail)


class ValidationError(HTTPException):
    def __init__(self, status_code: int = 404, detail: str = "Invalid input"):
        super().__init__(status_code, detail)


class ErrorSaving(HTTPException):
    def __init__(self, status_code: int = 400, detail: str = "Error saving data"):
        super().__init__(status_code, detail)
