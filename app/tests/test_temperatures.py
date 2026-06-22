from unittest.mock import AsyncMock, patch


@patch("app.routers.temperatures.fetch_current_temperature", new_callable=AsyncMock)
def test_update_temperatures_stores_records_for_each_city(mock_fetch, client):
    mock_fetch.return_value = 18.5
    city_a = client.post("/cities", json={"name": "Kyiv"}).json()
    city_b = client.post("/cities", json={"name": "London"}).json()

    response = client.post("/temperatures/update")
    assert response.status_code == 201
    records = response.json()
    assert {r["city_id"] for r in records} == {city_a["id"], city_b["id"]}
    assert all(r["temperature"] == 18.5 for r in records)


@patch("app.routers.temperatures.fetch_current_temperature", new_callable=AsyncMock)
def test_list_temperatures_filtered_by_city(mock_fetch, client):
    mock_fetch.return_value = 10.0
    city_a = client.post("/cities", json={"name": "Kyiv"}).json()
    client.post("/cities", json={"name": "London"})
    client.post("/temperatures/update")

    response = client.get("/temperatures", params={"city_id": city_a["id"]})
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["city_id"] == city_a["id"]


@patch("app.routers.temperatures.fetch_current_temperature", new_callable=AsyncMock)
def test_update_temperatures_skips_city_on_lookup_failure(mock_fetch, client):
    from app.weather import WeatherLookupError

    mock_fetch.side_effect = WeatherLookupError("not found")
    client.post("/cities", json={"name": "Unknownville"})

    response = client.post("/temperatures/update")
    assert response.status_code == 201
    assert response.json() == []
