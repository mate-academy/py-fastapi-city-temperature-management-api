import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from city.crud import get_all_cities
from temperature import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from temperature.utils import get_temperature
from asyncio import gather


async def update_temperatures(db: AsyncSession) -> dict:
    cities = await get_all_cities(db=db)
    temperatures = await gather(*[
        models.Temperature(
            date_time=datetime.datetime.now(),
            city_id=city.id,
            temperature=await get_temperature(city.name)
        )
        for city in cities
    ])
    db.add_all(temperatures)
    await db.commit()
    return {"detail": "Temperatures are successfully updated"}


async def get_all_temperatures(
        db: AsyncSession,
        city_id: int | None
) -> list[schemas.Temperature]:
    query = select(models.Temperature).options(
        selectinload(models.Temperature.city))
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()
