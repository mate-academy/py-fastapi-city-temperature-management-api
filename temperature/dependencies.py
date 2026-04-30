from typing import AsyncGenerator

from httpx import AsyncClient


async def get_client() -> AsyncGenerator[AsyncClient, None]:
    client = AsyncClient(timeout=30.0)
    try:
        yield client
    finally:
        await client.aclose()
