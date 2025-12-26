import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from database.models import Base, CityModel
from database.sqlite import engine, get_context
from main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest_asyncio.fixture
async def session():
    async with engine.connect() as eng:
        await eng.run_sync(Base.metadata.create_all)

    async with get_context() as session:
        yield session

    async with engine.connect() as eng:
        await eng.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def seed_data(session):
    cities = [
        CityModel(name="Berlin", additional_info="Info"),
        CityModel(name="Kiev", additional_info="Capital")
    ]

    session.add_all(cities)
    await session.commit()
