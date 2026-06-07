from datetime import datetime
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from city import models, schemas


from dependencies import get_city_temperature


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> models.DBTemperature | None:
    return await db.scalar(
        select(models.DBTemperature).where(
            models.DBTemperature.city_id == city_id
        )
    )


async def update_temperatures(db: AsyncSession) -> list[models.DBTemperature]:
    result = await db.execute(select(models.DBCity))
    cities = result.scalars().all()
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                new_temp = await get_city_temperature(client, city.name)
            except ValueError as e:
                print(f"Помилка: {e}")
                continue
            queryset = select(models.DBTemperature).where(
                models.DBTemperature.city_id == city.id
            )
            res_temp = await db.scalar(queryset)
            if res_temp:
                res_temp.temperature = new_temp
                res_temp.date_time = datetime.utcnow()
            else:
                new_record = models.DBTemperature(
                    city_id=city.id,
                    temperature=new_temp,
                    date_time=datetime.utcnow(),
                )
                db.add(new_record)
        await db.commit()
    all_temps = await db.execute(select(models.DBTemperature))
    return all_temps.scalars().all()


async def get_temperature_list(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[models.DBTemperature]:
    queryset = select(models.DBTemperature).options(
        selectinload(models.DBTemperature.city)
    )
    if city_id:
        queryset = queryset.where(models.DBTemperature.city_id == city_id)
    temperatures = await db.scalars(queryset)

    return temperatures.all()
