from datetime import datetime
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.cities.models import CityModel
from app.temperatures.models import TemperatureModel
from app.temperatures.schemas import TemperatureCreate


async def get_all_temperatures(db: AsyncSession, city_id: int | None = None):
    query = select(TemperatureModel)
    if city_id is not None:
        query = query.filter(TemperatureModel.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def fetch_and_update_temperatures(db: AsyncSession):
    cities_result = await db.execute(select(CityModel))
    cities = cities_result.scalars().all()

    if not cities:
        return []

    inserted_records = []

    async with AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": 50.45,
                        "longitude": 30.52,
                        "current_weather": True,
                    },
                    timeout=5.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    current_weather = data.get("current_weather", {})
                    temp_value = current_weather.get("temperature")

                    if temp_value is not None:
                        record_data = TemperatureCreate(
                            city_id=city.id,
                            temperature=float(temp_value),
                            date_time=datetime.utcnow(),
                        )
                        db_record = TemperatureModel(**record_data.model_dump())
                        db.add(db_record)
                        inserted_records.append(db_record)
            except Exception:
                continue

    if inserted_records:
        await db.commit()
        for record in inserted_records:
            await db.refresh(record)

    return inserted_records
