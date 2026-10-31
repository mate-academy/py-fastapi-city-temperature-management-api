import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.weather import get_weather_client


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    def db_override():
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = db_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    engine.dispose()


def test_city_crud_and_validation(client):
    assert client.post('/cities', json={'name': ''}).status_code == 422
    response = client.post('/cities', json={'name': 'Kyiv', 'additional_info': 'Ukraine'})
    assert response.status_code == 201
    city = response.json()
    assert city['additional_info'] == 'Ukraine'
    assert client.get('/cities').json() == [city]
    assert client.delete(f"/cities/{city['id']}").status_code == 204
    assert client.delete(f"/cities/{city['id']}").status_code == 404


def test_update_filter_and_cascade(client):
    def handler(request):
        if 'geocoding' in request.url.host:
            return httpx.Response(200, json={'results': [{'latitude': 50, 'longitude': 30}, {'latitude': 1, 'longitude': 2}]})
        assert request.url.params['latitude'] == '50'
        return httpx.Response(200, json={'current': {'temperature_2m': 12.5, 'time': '2026-01-01T12:00'}})

    async def weather_override():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as weather:
            yield weather

    app.dependency_overrides[get_weather_client] = weather_override
    a = client.post('/cities', json={'name': 'Kyiv'}).json()
    b = client.post('/cities', json={'name': 'Paris'}).json()
    response = client.post('/temperatures/update')
    assert response.status_code == 200
    records = client.get('/temperatures').json()
    assert len(records) == 2
    assert {r['city_id'] for r in records} == {a['id'], b['id']}
    assert all(r['temperature'] == 12.5 and r['date_time'] for r in records)
    assert len(client.get('/temperatures', params={'city_id': a['id']}).json()) == 1
    client.delete(f"/cities/{a['id']}")
    assert client.get('/temperatures', params={'city_id': a['id']}).json() == []
    assert len(client.get('/temperatures').json()) == 1


def test_weather_failure_does_not_save_partial_results(client):
    def handler(request):
        if 'geocoding' in request.url.host:
            if request.url.params['name'] == 'Unknown':
                return httpx.Response(200, json={'results': []})
            return httpx.Response(200, json={'results': [{'latitude': 50, 'longitude': 30}]})
        return httpx.Response(200, json={'current': {'temperature_2m': 10, 'time': '2026-01-01T12:00'}})

    async def weather_override():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as weather:
            yield weather

    app.dependency_overrides[get_weather_client] = weather_override
    client.post('/cities', json={'name': 'Kyiv'})
    client.post('/cities', json={'name': 'Unknown'})
    assert client.post('/temperatures/update').status_code == 502
    assert client.get('/temperatures').json() == []


def test_upstream_http_error_and_empty_update(client):
    assert client.post('/temperatures/update').json() == []

    def handler(request):
        return httpx.Response(503)

    async def weather_override():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as weather:
            yield weather

    app.dependency_overrides[get_weather_client] = weather_override
    client.post('/cities', json={'name': 'Kyiv'})
    assert client.post('/temperatures/update').status_code == 502
    assert client.get('/temperatures').json() == []
