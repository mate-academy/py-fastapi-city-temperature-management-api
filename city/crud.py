import httpx
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models
from settings import settings


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_all_cities(db: AsyncSession):
    query = select(models.City).add_columns(
        models.City.id, models.City.name, models.City.additional_info
    )
    cities_list = await db.execute(query)
    return [city for city in cities_list.fetchall()]


async def get_single_city(db: AsyncSession, city_id: int):
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalar()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdate):
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    existing_city = result.scalars().first()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    existing_city.name = city.name
    existing_city.additional_info = city.additional_info

    db.add(existing_city)
    await db.commit()
    await db.refresh(existing_city)

    return existing_city


async def delete_city(db: AsyncSession, city_id: int):
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    existing_city = result.scalars().first()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(existing_city)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def fetch_temperature(city_id: int, city_name: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.WEATHER_URL,
                params={"q": city_name, "key": settings.WEATHER_API_KEY},
            )
            response_json = response.json()
            if response_json.get("current"):
                return city_id, response_json["current"]["temp_c"]
    except Exception as e:
        print(f"Error for update temperature for {city_name}: {e}")


async def get_temperatures(city_id: int | None, db: AsyncSession):
    query = select(models.Temperature).add_columns(
        models.Temperature.id,
        models.Temperature.city_id,
        models.Temperature.temperature,
        models.Temperature.date_time,
    )
    if city_id is None:
        result = await db.execute(query)
        return result.all()

    if isinstance(city_id, int) and city_id > 0:
        query = query.filter(models.Temperature.city_id == city_id)
        return await db.execute(query)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Something went wrong. Check your city_id...",
    )
