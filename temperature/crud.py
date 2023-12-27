from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from temperature.models import Temperature
from temperature.get_weather import get_weather


async def get_all_temperatures(db: AsyncSession):
    query = select(Temperature)
    temperatures = await db.execute(query)
    return temperatures.scalars().all()


async def get_temperatures_by_city_id(db: AsyncSession, city_id: int):
    query = select(Temperature).where(Temperature.city_id == city_id)
    temperatures = await db.execute(query)
    return temperatures.scalars().all()


async def update_temperatures(db: AsyncSession, city_id: int):
    try:
        city = await db.execute(select(City).where(City.id == city_id))
        city_id = city.scalar()
        temperature_value = await get_weather(city.name)

        if city_id:
            temperature = Temperature(
                date_time=datetime.now(),
                city_id=city_id,
                temperature=temperature_value,
            )
            db.add(temperature)
            await db.commit()
            temperatures = await get_temperatures_by_city_id(db, city_id)
            return temperatures
        else:
            raise HTTPException(
                status_code=404,
                detail=f"City with name {City.name} not found!",
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating temperatures: {str(e)}"
        )


async def update_temperatures_for_all_cities(db: AsyncSession):
    try:
        cities = await db.execute(select(City))
        cities = cities.scalars().all()

        for city in cities:
            await update_temperatures(db=db, city_id=city.id)

        return {"message": "Weather updated for all cities!"}
    except Exception as e:
        return {"error": f"Error updating weather for all cities: {str(e)}"}
