import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_and_read_city():
    # Test Create
    response = client.post(
        "/cities", json={"name": "Paris", "additional_info": "Capital of France"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Paris"
    assert "id" in data

    # Test Read List
    response = client.get("/cities")
    assert response.status_code == 200
    assert len(response.json()) == 1


@patch("app.services.fetch_temperatures_concurrently", new_callable=AsyncMock)
def test_update_temperatures(mock_fetch):
    # Create city
    client.post("/cities", json={"name": "Tokyo", "additional_info": "Japan"})

    # Mock external API response
    mock_fetch.return_value = {"Tokyo": 22.5}

    response = client.post("/temperatures/update")
    assert response.status_code == 200
    assert response.json()["updated_records_count"] == 1

    # Check database records
    response = client.get("/temperatures")
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["temperature"] == 22.5
