from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import httpx
from .models import Temperature
from city.crud import get_cities


async def get_temperatures(db: AsyncSession, city_id: int = None):
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def update_temperatures(db: AsyncSession):
    cities = await get_cities(db)

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(f"https://wttr.in/{city.name}?format=j1")
            data = response.json()
            temperature = float(data["current_condition"][0]["temp_C"])

            db_temp = Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature
            )
            db.add(db_temp)

    await db.commit()
