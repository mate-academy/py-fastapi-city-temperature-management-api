def test_update_temperatures(api_client):
    api_client.post(
        "/cities",
        json={"name": "Berlin", "additional_info": "Germany"}
    )

    response = api_client.post("/temperatures/update")

    assert response.status_code == 200
    assert response.json()["records_created"] >= 1


def test_get_temperatures(api_client):
    response = api_client.get("/temperatures")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_temperatures_by_city_id(api_client):
    # create two cities
    city1 = api_client.post(
        "/cities",
        json={"name": "Paris", "additional_info": "France"}
    ).json()

    city2 = api_client.post(
        "/cities",
        json={"name": "Madrid", "additional_info": "Spain"}
    ).json()

    # update temperatures for all cities
    api_client.post("/temperatures/update")

    # fetch temperatures only for city1
    response = api_client.get(f"/temperatures?city_id={city1['id']}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # ensure all records belong to city1
    for record in data:
        assert record["city_id"] == city1["id"]
