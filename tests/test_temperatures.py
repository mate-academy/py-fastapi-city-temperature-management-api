async def test_update_and_list_temperatures(client):
    kyiv = (await client.post("/cities", json={"name": "Kyiv"})).json()
    lviv = (await client.post("/cities", json={"name": "Lviv"})).json()
    unknown = (await client.post("/cities", json={"name": "Atlantis"})).json()

    response = await client.post("/temperatures/update")
    assert response.status_code == 200
    body = response.json()
    assert {t["city_id"]: t["temperature"] for t in body["updated"]} == {
        kyiv["id"]: 12.5,
        lviv["id"]: 9.1,
    }
    assert [f["city_id"] for f in body["failed"]] == [unknown["id"]]

    response = await client.get("/temperatures/")
    assert len(response.json()) == 2

    response = await client.get(f"/temperatures/?city_id={kyiv['id']}")
    records = response.json()
    assert len(records) == 1
    assert records[0]["temperature"] == 12.5


async def test_temperatures_for_missing_city(client):
    response = await client.get("/temperatures/?city_id=999")
    assert response.status_code == 404


async def test_deleting_city_deletes_its_temperatures(client):
    kyiv = (await client.post("/cities", json={"name": "Kyiv"})).json()
    await client.post("/temperatures/update")
    await client.delete(f"/cities/{kyiv['id']}")
    response = await client.get("/temperatures/")
    assert response.json() == []
