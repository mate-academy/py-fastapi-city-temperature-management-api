import asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.orm import Session
from Temperature import models
from City.models import DBCity
from settings import settings

load_dotenv()

async def fetch_temperature(client: AsyncClient, city: DBCity):
    res = await client.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={settings.API_KEY}&units=metric")
    res.raise_for_status()
    return res.json()["main"]["temp"]


async def create_temperature(db: Session, client: AsyncClient):
    cities = db.query(DBCity).all()

    temps = await asyncio.gather(
        *(fetch_temperature(client, i) for i in cities),
        return_exceptions=True,
    )

    for city, temp in zip(cities, temps):
        if isinstance(temp, Exception):
            continue
        db.add(models.Temperature(city_id=city.id, temperature=temp))
    db.commit()
    return db.query(models.Temperature).all()


def retrieve_temp(db: Session, city_id: int | None):
    queryset = db.query(models.Temperature)
    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)
    return queryset.all()