import pytest
from sqlalchemy import select

from database.models import CityModel


@pytest.mark.asyncio
async def test_post(client, session):
    response = await client.post(url="/cities/", json={"name": "Berlin"})
    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["name"] == "Berlin"

    response = await client.post(url="/cities/", json={"name": "Moscow", "additional_info": "something"})
    assert response.status_code == 201
    assert response.json()["id"] == 4
    assert response.json()["name"] == "Moscow"
    assert response.json()["additional_info"] == "something"


@pytest.mark.asyncio
async def test_get_cities(client, session, seed_data):
    response = await client.get(url="/cities/")
    assert response.status_code == 200
    assert len(response.json()["cities"]) == 2

    model = response.json()["cities"][0]
    assert model["name"] == "Berlin"
    assert model["additional_info"] == "Info"
    assert model["id"] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "city_id, name, additional_info",
    [
        (1, "Berlin", "Info"),
        (2, "Kiev", "Capital")
    ]
)
async def test_get_city_by_id(client, session, seed_data, city_id, name, additional_info):
    response = await client.get(url=f"/cities/{city_id}/")
    city = response.json()
    assert response.status_code == 200
    assert city["name"] == name
    assert city["additional_info"] == additional_info


@pytest.mark.asyncio
async def test_put(client, seed_data, session):
    response = await client.put(
        url="/cities/1/",
        json={"name": "NameWrong", "additional_info": "InfoWrong"}
    )

    assert response.status_code == 200
    city = await session.get(CityModel, 1)
    assert city.name == "NameWrong"
    assert city.additional_info == "InfoWrong"


@pytest.mark.asyncio
async def test_delete(client, session, seed_data):
    city_1 = await session.get(CityModel, 1)
    city_2 = await session.get(CityModel, 2)

    response = await client.delete(url="/cities/2/")
    assert response.status_code == 200

    response = await client.get(url="/cities/")
    assert len(response.json()["cities"]) == 1

    cities = await session.execute(select(CityModel))
    cities = cities.scalars().all()
    assert city_2 not in cities
    assert city_1 in cities
