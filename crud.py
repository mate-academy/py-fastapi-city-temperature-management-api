from app import models, schemas
from app.weather import fetch_temperature
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_city(session: AsyncSession, city: schemas.CityCreate):
    city_data = city.model_dump()
    db_city = models.City(**city_data)
    session.add(db_city)
    await session.commit()
    await session.refresh(db_city)
    return db_city

async def get_cities(session: AsyncSession, skip: int = 0, limit: int = 5):
    result = await session.scalars(select(models.City).offset(skip).limit(limit))
    return result.all()

async def get_all_cities(session: AsyncSession):
    result = await session.scalars(select(models.City))
    return result.all()

async def get_city_by_id(session: AsyncSession, city_id: int):
    result = await session.scalars(select(models.City).where(models.City.id == city_id))
    return result.one_or_none()

async def get_city_by_name(session: AsyncSession, name: str):
    result = await session.scalars(select(models.City).where(models.City.name == name))
    return result.one_or_none()

async def update_city_by_id(session: AsyncSession, city_id: int, city: schemas.CityUpdate):
    result = await session.scalars(select(models.City).where(models.City.id == city_id))
    city_db = result.one_or_none()

    if city_db is None:
        raise ValueError("No city found")

    for field, value in city.model_dump(exclude_unset=True).items():
        if field == "name" and value is None:
            raise ValueError("City cannot be None")
        
        setattr(city_db, field, value)

    await session.commit()
    await session.refresh(city_db)
    return city_db

async def delete_city(session: AsyncSession, city_id: int):
    result = await session.scalars(select(models.City).where(models.City.id == city_id))
    city_db = result.one_or_none()

    if city_db is None:
        raise ValueError("No city found")

    await session.delete(city_db)
    await session.commit()
    return f"City successfully deleted"

async def add_temperature(session: AsyncSession, temperature: schemas.TemperatureCreate):
    query = select(models.City).where(models.City.id == temperature.city_id)
    result = await session.execute(query)
    city = result.scalar_one_or_none()

    if city is None:
        raise ValueError("No city found")

    temperature_data = temperature.model_dump()
    db_temperature = models.Temperature(**temperature_data)
    session.add(db_temperature)
    await session.commit()
    await session.refresh(db_temperature)
    return db_temperature

async def get_temperatures(session: AsyncSession, skip: int = 0, limit: int = 5):
    result = await session.scalars(select(models.Temperature).offset(skip).limit(limit))
    return result.all()

async def get_temperature_by_city_id(session: AsyncSession, city_id: int):
    result = await session.scalars(select(models.Temperature).where(models.Temperature.city_id == city_id))
    return result.all()

async def update_all_temperatures(session: AsyncSession):
    cities = await get_all_cities(session)

    if not cities:
        return []

    temperatures = []

    for city in cities:
        current_temperature = await fetch_temperature(city.name)

        db_temperature = models.Temperature(
            city_id=city.id,
            temperature=current_temperature,
        )
        session.add(db_temperature)
        temperatures.append(db_temperature)

    await session.commit()

    for temperature in temperatures:
        await session.refresh(temperature)

    return temperatures