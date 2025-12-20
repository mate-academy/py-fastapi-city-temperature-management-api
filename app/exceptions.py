"""
Error handlers for FastAPI application.
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
