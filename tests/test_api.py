from collections.abc import Generator
from datetime import UTC, datetime

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.services.weather import (
    CurrentTemperature,
    WeatherServiceError,
    get_weather_service,
)


class FakeWeatherService:
    async def fetch_current_temperature(self, city_name: str) -> CurrentTemperature:
        readings = {"Dublin": 12.5, "Kyiv": 8.0}
        return CurrentTemperature(
            date_time=datetime(2025, 1, 2, 12, 0, tzinfo=UTC),
            temperature=readings[city_name],
        )


class FailingWeatherService:
    async def fetch_current_temperature(self, city_name: str) -> CurrentTemperature:
        raise WeatherServiceError(f"city '{city_name}' was not found")


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=test_engine)

    def override_db() -> Generator[Session, None, None]:
        with TestingSession() as session:
            yield session

    async def override_weather():
        yield FakeWeatherService()

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_weather_service] = override_weather
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_city_crud(client: TestClient) -> None:
    create_response = client.post(
        "/cities",
        json={"name": "  Dublin  ", "additional_info": "Ireland"},
    )
    assert create_response.status_code == 201
    assert create_response.json() == {
        "id": 1,
        "name": "Dublin",
        "additional_info": "Ireland",
    }

    assert client.get("/cities").json() == [create_response.json()]
    assert client.get("/cities/1").json() == create_response.json()

    update_response = client.put(
        "/cities/1",
        json={"additional_info": "Capital of Ireland"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["additional_info"] == "Capital of Ireland"

    assert client.delete("/cities/1").status_code == 204
    assert client.get("/cities/1").status_code == 404


def test_temperature_update_and_filter(client: TestClient) -> None:
    for name in ("Dublin", "Kyiv"):
        assert client.post("/cities", json={"name": name}).status_code == 201

    update_response = client.post("/temperatures/update")
    assert update_response.status_code == 201
    assert len(update_response.json()) == 2
    assert {item["temperature"] for item in update_response.json()} == {12.5, 8.0}

    all_temperatures = client.get("/temperatures").json()
    dublin_temperatures = client.get("/temperatures", params={"city_id": 1}).json()
    assert len(all_temperatures) == 2
    assert len(dublin_temperatures) == 1
    assert dublin_temperatures[0]["city_id"] == 1

    assert client.delete("/cities/1").status_code == 204
    remaining = client.get("/temperatures").json()
    assert len(remaining) == 1
    assert remaining[0]["city_id"] == 2


def test_failed_temperature_update_is_not_partially_saved(client: TestClient) -> None:
    assert client.post("/cities", json={"name": "Unknown"}).status_code == 201

    async def override_failing_weather():
        yield FailingWeatherService()

    app.dependency_overrides[get_weather_service] = override_failing_weather

    response = client.post("/temperatures/update")
    assert response.status_code == 502
    assert response.json()["detail"] == "city 'Unknown' was not found"
    assert client.get("/temperatures").json() == []


def test_validation_and_missing_city(client: TestClient) -> None:
    assert client.post("/cities", json={"name": "   "}).status_code == 422
    assert client.delete("/cities/999").status_code == 404
    assert client.get("/temperatures", params={"city_id": 0}).status_code == 422
