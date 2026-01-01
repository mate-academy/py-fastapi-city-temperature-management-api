def test_create_city(api_client):
    response = api_client.post(
        "/cities",
        json={
            "name": "Kyiv",
            "additional_info": "Capital of Ukraine"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Kyiv"
    assert "id" in data


def test_get_cities(api_client):
    response = api_client.get("/cities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_city_by_id(api_client):
    create_response = api_client.post(
        "/cities",
        json={"name": "Lviv", "additional_info": "Historic city"}
    )
    city_id = create_response.json()["id"]

    response = api_client.get(f"/cities/{city_id}")
    assert response.status_code == 200
    assert response.json()["id"] == city_id


def test_delete_city(api_client):
    create_response = api_client.post(
        "/cities",
        json={"name": "Odessa", "additional_info": "Port city"}
    )
    city_id = create_response.json()["id"]

    delete_response = api_client.delete(f"/cities/{city_id}")
    assert delete_response.status_code == 204


def test_create_duplicate_city(api_client):
    api_client.post(
        "/cities",
        json={"name": "Kharkiv", "additional_info": "First"}
    )

    response = api_client.post(
        "/cities",
        json={"name": "Kharkiv", "additional_info": "Duplicate"}
    )

    assert response.status_code == 409


def test_get_nonexistent_city(api_client):
    response = api_client.get("/cities/999")
    assert response.status_code == 404


def test_delete_nonexistent_city(api_client):
    response = api_client.delete("/cities/999")
    assert response.status_code == 404
