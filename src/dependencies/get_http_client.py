from fastapi import Request
from httpx import AsyncClient


async def get_http_client(request: Request) -> AsyncClient:
    return request.app.state.http_client
