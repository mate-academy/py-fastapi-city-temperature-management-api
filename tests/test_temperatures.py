from fastapi.testclient import TestClient

from app.dependencies import get_db
from app.main import app
from app.database import SessionLocal, engine
from app.models import Base

client = TestClient(app)

# Create the database tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_update_temperatures():
    response = client.post("/temperatures/update")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_temperatures():
    response = client.get("/temperatures/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_temperatures_by_city():
    response = client.post(
        "/cities/", json={"name": "Test City", "additional_info": "Some info"}
    )
    city_id = response.json()["id"]
    response = client.get(f"/temperatures/by_city?city_id={city_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
