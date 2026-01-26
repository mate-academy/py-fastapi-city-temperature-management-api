import httpx
from fastapi import HTTPException
from httpx import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from cities import schemas
from cities import models
from cities.models import DBCity


async def get_cities_list(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))

    return cities.all()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.DBCity:
     async with httpx.AsyncClient() as client:
        url = create_url_for_check_city_exist(city=city.name)
        response = await send_request_for_check_city_exist(data=url, client=client)

        if response.status_code != 200:
            response_data = response.json()
            massage = response_data.get("error",{}).get("message")
            raise HTTPException(
                status_code=response.status_code,
                detail=massage
            )

     db_city = models.DBCity(
         name=city.name,
         additional_info=city.additional_info,
     )

     db.add(db_city)
     await db.commit()
     await db.refresh(db_city)
     return db_city


async def get_city_by_name(db: AsyncSession, city_name: str)-> models.DBCity | None:
    return await db.scalar(select(models.DBCity).where(models.DBCity.name == city_name))


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.DBCity | None:
    return await db.scalar(select(models.DBCity).where(models.DBCity.id == city_id))


async def update_city(db: AsyncSession, db_city: DBCity, city: schemas.CityBase) -> models.DBCity:
    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city: DBCity) -> None:
    await db.delete(city)
    await db.commit()


def create_url_for_check_city_exist(city: str) -> dict:
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": settings.WEATHER_API_KEY,
        "q": city,
        "aqi": "no"
    }
    return {"url": url, "params": params}


async def send_request_for_check_city_exist(data: dict, client: httpx.AsyncClient) -> Response:
    return await client.get(url=data["url"], params=data["params"])
