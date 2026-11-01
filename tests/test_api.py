import pytest

from app.temperature import router as temperature_router


@pytest.mark.asyncio
async def test_city_crud(client):
    create_response = await client.post(
        "/cities",
        json={
            "name": "Kyiv",
            "additional_info": "Capital of Ukraine",
        },
    )
    assert create_response.status_code == 201
    city_id = create_response.json()["id"]

    list_response = await client.get("/cities")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    detail_response = await client.get(f"/cities/{city_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["name"] == "Kyiv"

    update_response = await client.put(
        f"/cities/{city_id}",
        json={
            "name": "Kyiv City",
            "additional_info": "Updated information",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Kyiv City"

    delete_response = await client.delete(f"/cities/{city_id}")
    assert delete_response.status_code == 204

    missing_response = await client.get(f"/cities/{city_id}")
    assert missing_response.status_code == 404


@pytest.mark.asyncio
async def test_temperature_update_filter_and_cascade_delete(
    client,
    monkeypatch,
):
    city_ids = []
    for city_name in ("Kyiv", "Lviv"):
        response = await client.post(
            "/cities",
            json={"name": city_name},
        )
        assert response.status_code == 201
        city_ids.append(response.json()["id"])

    temperatures = {"Kyiv": 12.5, "Lviv": 10.0}

    async def fake_get_current_temperature(city_name, client):
        return temperatures[city_name]

    monkeypatch.setattr(
        temperature_router,
        "get_current_temperature",
        fake_get_current_temperature,
    )

    update_response = await client.post("/temperatures/update")
    assert update_response.status_code == 200
    assert sorted(
        record["temperature"] for record in update_response.json()
    ) == [10.0, 12.5]

    filter_response = await client.get(
        "/temperatures",
        params={"city_id": city_ids[0]},
    )
    assert filter_response.status_code == 200
    assert len(filter_response.json()) == 1
    assert filter_response.json()[0]["temperature"] == 12.5

    delete_response = await client.delete(f"/cities/{city_ids[0]}")
    assert delete_response.status_code == 204

    deleted_city_temperatures = await client.get(
        "/temperatures",
        params={"city_id": city_ids[0]},
    )
    assert deleted_city_temperatures.status_code == 200
    assert deleted_city_temperatures.json() == []


@pytest.mark.asyncio
async def test_temperature_update_requires_api_key(
    client,
    monkeypatch,
):
    create_response = await client.post(
        "/cities",
        json={"name": "Kyiv"},
    )
    assert create_response.status_code == 201

    monkeypatch.delenv("WEATHER_API_KEY", raising=False)

    response = await client.post("/temperatures/update")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Weather API key is not configured",
    }
