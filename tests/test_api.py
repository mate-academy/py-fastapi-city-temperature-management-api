from datetime import datetime
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

from app.services.weather import CityWeatherResult, WeatherReading, WeatherServiceError

KYIV_TZ = ZoneInfo("Europe/Kyiv")


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_cities(client):
    response = client.post(
        "/cities",
        json={"name": "Kyiv", "additional_info": "Capital of Ukraine"},
    )
    assert response.status_code == 201
    city = response.json()
    assert city["id"] == 1
    assert city["name"] == "Kyiv"
    assert city["additional_info"] == "Capital of Ukraine"

    response = client.get("/cities")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_duplicate_city_returns_409(client):
    client.post("/cities", json={"name": "Lviv", "additional_info": ""})
    response = client.post("/cities", json={"name": "Lviv", "additional_info": ""})
    assert response.status_code == 409


def test_get_update_delete_city(client):
    created = client.post(
        "/cities",
        json={"name": "Odesa", "additional_info": "Port city"},
    ).json()
    city_id = created["id"]

    response = client.get(f"/cities/{city_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Odesa"

    response = client.put(
        f"/cities/{city_id}",
        json={"additional_info": "Black Sea port"},
    )
    assert response.status_code == 200
    assert response.json()["additional_info"] == "Black Sea port"
    assert response.json()["name"] == "Odesa"

    response = client.delete(f"/cities/{city_id}")
    assert response.status_code == 204

    response = client.get(f"/cities/{city_id}")
    assert response.status_code == 404


def test_get_missing_city_returns_404(client):
    response = client.get("/cities/999")
    assert response.status_code == 404


def test_list_temperatures_empty(client):
    response = client.get("/temperatures")
    assert response.status_code == 200
    assert response.json() == []


def test_list_temperatures_unknown_city_returns_404(client):
    response = client.get("/temperatures", params={"city_id": 999})
    assert response.status_code == 404


def test_update_temperatures_with_no_cities(client):
    response = client.post("/temperatures/update")
    assert response.status_code == 200
    assert response.json() == {"temperatures": [], "errors": []}


def test_update_temperatures_success_and_filter(client):
    kyiv = client.post(
        "/cities",
        json={"name": "Kyiv", "additional_info": ""},
    ).json()
    lviv = client.post(
        "/cities",
        json={"name": "Lviv", "additional_info": ""},
    ).json()

    mock_results = [
        CityWeatherResult(
            city_id=kyiv["id"],
            city_name="Kyiv",
            reading=WeatherReading(
                temperature=12.5,
                date_time=datetime(2026, 3, 15, 14, 0, tzinfo=KYIV_TZ),
            ),
        ),
        CityWeatherResult(
            city_id=lviv["id"],
            city_name="Lviv",
            reading=WeatherReading(
                temperature=10.0,
                date_time=datetime(2026, 3, 15, 14, 0, tzinfo=KYIV_TZ),
            ),
        ),
    ]

    with patch(
        "app.routers.temperatures.fetch_temperatures_for_cities",
        new=AsyncMock(return_value=mock_results),
    ):
        response = client.post("/temperatures/update")

    assert response.status_code == 200
    payload = response.json()
    assert payload["errors"] == []
    assert len(payload["temperatures"]) == 2

    response = client.get("/temperatures")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/temperatures", params={"city_id": kyiv["id"]})
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["city_id"] == kyiv["id"]
    assert records[0]["temperature"] == 12.5


def test_update_temperatures_partial_errors(client):
    client.post("/cities", json={"name": "Kyiv", "additional_info": ""})
    client.post("/cities", json={"name": "Atlantis", "additional_info": ""})

    mock_results = [
        CityWeatherResult(
            city_id=1,
            city_name="Kyiv",
            reading=WeatherReading(
                temperature=5.0,
                date_time=datetime(2026, 3, 15, 12, 0, tzinfo=KYIV_TZ),
            ),
        ),
        CityWeatherResult(
            city_id=2,
            city_name="Atlantis",
            error="City 'Atlantis' was not found by the weather provider",
        ),
    ]

    with patch(
        "app.routers.temperatures.fetch_temperatures_for_cities",
        new=AsyncMock(return_value=mock_results),
    ):
        response = client.post("/temperatures/update")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["temperatures"]) == 1
    assert len(payload["errors"]) == 1
    assert "Atlantis" in payload["errors"][0]


def test_update_temperatures_provider_unavailable(client):
    client.post("/cities", json={"name": "Kyiv", "additional_info": ""})

    with patch(
        "app.routers.temperatures.fetch_temperatures_for_cities",
        new=AsyncMock(side_effect=WeatherServiceError("Weather provider is unavailable")),
    ):
        response = client.post("/temperatures/update")

    assert response.status_code == 502


def test_delete_city_cascades_temperatures(client):
    city = client.post(
        "/cities",
        json={"name": "Kharkiv", "additional_info": ""},
    ).json()

    mock_results = [
        CityWeatherResult(
            city_id=city["id"],
            city_name="Kharkiv",
            reading=WeatherReading(
                temperature=3.0,
                date_time=datetime(2026, 3, 15, 10, 0, tzinfo=KYIV_TZ),
            ),
        ),
    ]

    with patch(
        "app.routers.temperatures.fetch_temperatures_for_cities",
        new=AsyncMock(return_value=mock_results),
    ):
        client.post("/temperatures/update")

    assert len(client.get("/temperatures").json()) == 1

    response = client.delete(f"/cities/{city['id']}")
    assert response.status_code == 204
    assert client.get("/temperatures").json() == []
