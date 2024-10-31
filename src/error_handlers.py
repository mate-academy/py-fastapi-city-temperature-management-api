from fastapi import Request
from fastapi.responses import JSONResponse
from src.exceptions import CityNotFoundError, KeyNotConfigure


async def handle_city_not_found(
    request: Request,
    exc: CityNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


async def handle_key_not_configured(
    request: Request,
    exc: KeyNotConfigure
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"message": exc.message},
    )
