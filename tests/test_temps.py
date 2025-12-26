import pytest


@pytest.mark.asyncio
async def test_update_temperatures(client):
    response = await client.post(url="/temperatures/update/")
    assert response.status_code == 200
    assert response.json()["detail"] == "All Cities updated successfully!"


    response = await client.get(url="/temperatures/")
    assert response.status_code == 200

    json = response.json()["temps"]

    for ls in json:
        assert "city_id" in ls
        assert "date_time" in ls
        assert "temperature" in ls


@pytest.mark.asyncio
async def test_get_temps_for_city(client):
    response = await client.get(url="/temperatures/", params={"city_id": 1})
    assert response.status_code == 200
    assert len(response.json()["temps"]) == 0

    await client.post(url="/temperatures/update/") # 1
    await client.post(url="/temperatures/update/") # 2

    response = await client.get(url="/temperatures/", params={"city_id": 1})
    assert response.status_code == 200

    assert len(response.json()["temps"]) == 2

