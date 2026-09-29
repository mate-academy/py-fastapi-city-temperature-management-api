async def test_city_crud(client):
    response = await client.post(
        "/cities", json={"name": "Kyiv", "additional_info": "Capital"}
    )
    assert response.status_code == 201
    city = response.json()
    assert city["name"] == "Kyiv"

    response = await client.get("/cities")
    assert response.json() == [city]

    response = await client.get(f"/cities/{city['id']}")
    assert response.json() == city

    response = await client.put(
        f"/cities/{city['id']}", json={"additional_info": "Capital of Ukraine"}
    )
    assert response.status_code == 200
    assert response.json()["additional_info"] == "Capital of Ukraine"
    assert response.json()["name"] == "Kyiv"

    response = await client.delete(f"/cities/{city['id']}")
    assert response.status_code == 204
    response = await client.get(f"/cities/{city['id']}")
    assert response.status_code == 404


async def test_duplicate_city_name_is_rejected(client):
    await client.post("/cities", json={"name": "Kyiv"})
    response = await client.post("/cities", json={"name": "Kyiv"})
    assert response.status_code == 409

    other = (await client.post("/cities", json={"name": "Lviv"})).json()
    response = await client.put(f"/cities/{other['id']}", json={"name": "Kyiv"})
    assert response.status_code == 409


async def test_invalid_city_payload(client):
    assert (await client.post("/cities", json={"name": ""})).status_code == 422
    city = (await client.post("/cities", json={"name": "Kyiv"})).json()
    response = await client.put(f"/cities/{city['id']}", json={"name": None})
    assert response.status_code == 422


async def test_missing_city_returns_404(client):
    assert (await client.get("/cities/999")).status_code == 404
    assert (await client.put("/cities/999", json={})).status_code == 404
    assert (await client.delete("/cities/999")).status_code == 404
