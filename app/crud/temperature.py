from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.city import City
from app.models.temperature import Temperature
from app.schemas.temperature import TemperatureCreateSchema


async def get_all_temperatures(db: AsyncSession):
    """
    Отримує список усіх записів температури з бази даних.
    """
    result = await db.execute(select(Temperature))
    return result.scalars().all()


async def get_temperature_with_city_id(db: AsyncSession, city_id: int):

    city = await db.get(City, city_id)

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )

    result = await db.execute(select(Temperature).where(Temperature.city_id == city_id))
    temperatures = result.scalars().all()

    if not temperatures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No temperature records found for city with id {city_id}"
        )

    return temperatures


async def create_temperature_record(db: AsyncSession, temp_data: TemperatureCreateSchema) -> Temperature:
    city_exists = await db.get(City, temp_data.city_id)
    if not city_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {temp_data.city_id} not found"
        )

    new_temperature = Temperature(
        city_id=temp_data.city_id,
        date_time=temp_data.date_time,
        temperature=temp_data.temperature
    )

    try:
        db.add(new_temperature)
        await db.commit()
        await db.refresh(new_temperature)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating temperature record: {e}"
        )
    return new_temperature


async def fetch_and_store_temperatures(db: AsyncSession):

    all_cities_result = await db.execute(select(City))
    cities = all_cities_result.scalars().all()

    if not cities:
        return {"message": "No cities found in the database to fetch temperatures for."}

    fetched_data = []
    for city_obj in cities:
        try:
            current_temp = 20.0 + (city_obj.id * 0.5) # Заглушка, змінити на реальний виклик API

            temp_record_data = TemperatureCreateSchema(
                city_id=city_obj.id,
                date_time=datetime.now(timezone.utc),
                temperature=current_temp
            )

            await create_temperature_record(db, temp_record_data)
            fetched_data.append(
                {"city_name": city_obj.name, "temperature": current_temp, "status": "success"}
            )
        except Exception as e:
            fetched_data.append(
                {"city_name": city_obj.name, "status": "failed", "error": str(e)}
            )
            print(f"Error fetching temperature for {city_obj.name}: {e}")

    return {"message": "Temperature data updated for cities.", "details": fetched_data}