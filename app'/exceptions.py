"""
Error handlers for FastAPI application.
"""
import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
        Handler for HTTPException (404, 400, etc.).
        """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler for data validation errors (422 Unprocessable Entity).
    """
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Data validation error",
            "errors": exc.errors(),
            "body": exc.body
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler for unexpected errors (500 Internal Server Error).
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status_code": 500
        }
    )


# Helper functions for creating standard errors
def not_found_error(resource: str, resource_id: int = None) -> HTTPException:
    """
    Creates HTTPException for 404 Not Found error.
    """
    detail = f"{resource} not found"
    if resource_id is not None:
        detail = f"{resource} with id {resource_id} not found"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def bad_request_error(detail: str) -> HTTPException:
    """
    Creates HTTPException for 400 Bad Request error.
    """
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
