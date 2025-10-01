from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.weather.schemas import WeatherData
from src.temperature.models import DbTemperature



def get_all_selection() -> Select:
    return select(DbTemperature)

def filter_by_city_id(selection: Select, city_id: int | None) -> Select:
    if city_id is not None:
        selection = selection.where(DbTemperature.city_id == city_id)
    return selection

async def create_temperature(
        db: AsyncSession,
        city_id,
        temperature_data: WeatherData
) -> DbTemperature:
    new_temp = DbTemperature(
        city_id=city_id,
        temperature=temperature_data.temperature,
        date_time=temperature_data.date_time,
    )
    db.add(new_temp)
    await db.commit()
    await db.refresh(new_temp)
    return new_temp

async def read_cities_temperatures(db: AsyncSession, city_id: int | None) -> list[DbTemperature]:
    selection = get_all_selection()
    selection = filter_by_city_id(selection, city_id)
    result = await db.execute(selection)
    return result.scalars().all()
