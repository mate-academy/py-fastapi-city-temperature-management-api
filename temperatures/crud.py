from sqlalchemy import select
from temperatures.models import Temperature


async def get_temperature(db, city_id: int = None):
    query = select(Temperature)
    if city_id:
        query = query.where(Temperature.city_id == city_id)
    result =  await db.execute(query)
    temperatures = result.scalars().all()
    return temperatures

async def create_temperature(db, city_id, temperature, date_time):
    db_temperature = Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time,
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature
