from datetime import datetime

from fastapi.testclient import TestClient

from app.services import CurrentWeather, WeatherServiceError


def test_city_crud(client: TestClient) -> None:
    created = client.post(
        "/cities", json={"name": "Kyiv", "additional_info": "Capital of Ukraine"}
    )
    assert created.status_code == 201
    city_id = created.json()["id"]
    assert client.get("/cities").json() == [created.json()]
    assert client.get(f"/cities/{city_id}").json() == created.json()

    updated = client.put(
        f"/cities/{city_id}", json={"name": "Kyiv", "additional_info": "Updated"}
    )
    assert updated.json()["additional_info"] == "Updated"
    assert client.delete(f"/cities/{city_id}").status_code == 204
    assert client.get(f"/cities/{city_id}").status_code == 404


def test_duplicate_city_is_rejected(client: TestClient) -> None:
    payload = {"name": "Lviv", "additional_info": None}
    assert client.post("/cities", json=payload).status_code == 201
    assert client.post("/cities", json=payload).status_code == 409


def test_temperature_update_and_filter(client: TestClient, monkeypatch) -> None:
    first_id = client.post("/cities", json={"name": "Kyiv"}).json()["id"]
    second_id = client.post("/cities", json={"name": "Unknown"}).json()["id"]

    async def fake_fetch(_client, city_name: str):
        if city_name == "Unknown":
            raise WeatherServiceError("City 'Unknown' was not found")
        return CurrentWeather(datetime(2026, 1, 2, 12, 0), -1.5)

    monkeypatch.setattr("app.routers.temperatures.fetch_current_temperature", fake_fetch)
    response = client.post("/temperatures/update")
    assert len(response.json()["created"]) == 1
    assert response.json()["errors"] == {str(second_id): "City 'Unknown' was not found"}
    assert client.get(f"/temperatures?city_id={first_id}").json()[0]["temperature"] == -1.5
    assert client.get(f"/temperatures?city_id={second_id}").json() == []


def test_delete_city_cascades_temperatures(client: TestClient, monkeypatch) -> None:
    city_id = client.post("/cities", json={"name": "Odesa"}).json()["id"]

    async def fake_fetch(_client, _city_name: str):
        return CurrentWeather(datetime(2026, 1, 2, 12, 0), 5.0)

    monkeypatch.setattr("app.routers.temperatures.fetch_current_temperature", fake_fetch)
    client.post("/temperatures/update")
    client.delete(f"/cities/{city_id}")
    assert client.get("/temperatures").json() == []
