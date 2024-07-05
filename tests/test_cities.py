from fastapi.testclient import TestClient

from app.dependencies import get_db
from app.main import app
from app.database import SessionLocal, engine
from app.models import Base

client = TestClient(app)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_city():
    response = client.post(
        "/cities/", json={"name": "Test City", "additional_info": "Some info"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test City"
    assert response.json()["additional_info"] == "Some info"


def test_read_cities():
    response = client.get("/cities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_city():
    response = client.post(
        "/cities/", json={"name": "Test City", "additional_info": "Some info"}
    )
    city_id = response.json()["id"]
    response = client.get(f"/cities/{city_id}")
    assert response.status_code == 200
    assert response.json()["id"] == city_id


def test_delete_city():
    response = client.post(
        "/cities/", json={"name": "Test City", "additional_info": "Some info"}
    )
    city_id = response.json()["id"]
    response = client.delete(f"/cities/{city_id}")
    assert response.status_code == 200
    assert response.json()["id"] == city_id
