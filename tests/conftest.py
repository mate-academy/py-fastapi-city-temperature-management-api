from typing import AsyncGenerator

import httpx
import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.database import Base, _enable_sqlite_foreign_keys
from app.dependencies import get_db, get_http_client
from app.main import app

FAKE_CITIES = {"Kyiv": (50.45, 30.52, 12.5), "Lviv": (49.84, 24.03, 9.1)}


def fake_weather_api(request: httpx.Request) -> httpx.Response:
    params = request.url.params
    if "geocoding" in request.url.host:
        city = FAKE_CITIES.get(params["name"])
        if city is None:
            return httpx.Response(200, json={})
        return httpx.Response(
            200, json={"results": [{"latitude": city[0], "longitude": city[1]}]}
        )
    latitude = float(params["latitude"])
    temperature = next(t for lat, _, t in FAKE_CITIES.values() if lat == latitude)
    return httpx.Response(
        200,
        json={"current": {"time": "2026-09-29T12:00", "temperature_2m": temperature}},
    )


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    event.listen(engine.sync_engine, "connect", _enable_sqlite_foreign_keys)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    async def override_get_http_client():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(fake_weather_api)
        ) as http_client:
            yield http_client

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_http_client] = override_get_http_client
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    await engine.dispose()
