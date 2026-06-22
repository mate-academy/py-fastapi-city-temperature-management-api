def test_create_and_list_city(client):
    response = client.post("/cities", json={"name": "Kyiv", "additional_info": "Ukraine"})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Kyiv"
    assert body["id"] is not None

    response = client.get("/cities")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_duplicate_city_returns_409(client):
    client.post("/cities", json={"name": "Kyiv"})
    response = client.post("/cities", json={"name": "Kyiv"})
    assert response.status_code == 409


def test_get_missing_city_returns_404(client):
    response = client.get("/cities/999")
    assert response.status_code == 404


def test_update_city(client):
    created = client.post("/cities", json={"name": "Kyiv"}).json()
    response = client.put(
        f"/cities/{created['id']}", json={"name": "Kyiv", "additional_info": "updated"}
    )
    assert response.status_code == 200
    assert response.json()["additional_info"] == "updated"


def test_delete_city(client):
    created = client.post("/cities", json={"name": "Kyiv"}).json()
    response = client.delete(f"/cities/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/cities/{created['id']}").status_code == 404
