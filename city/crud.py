from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.DBCity:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityUpdate
) -> models.DBCity:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    db_city = result.scalar()

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.DBCity:
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city(db: AsyncSession, city_id: int) -> str:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    result = await db.execute(query)
    db_city = result.scalar()

    await db.delete(db_city)
    await db.commit()

    return "Successfully deleted"


async def get_all_temperature_records(db: AsyncSession) -> list[models.DBTemperature]:
    query = select(models.DBTemperature).options(selectinload(models.DBTemperature.city))
    result = await db.execute(query)
    return result.scalars().all()


async def create_temperature_by_city_id(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
) -> schemas.Temperature:
    query = insert(models.DBTemperature).values(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time
    )
    result = await db.execute(query)
    city = await get_city_by_id(db=db, city_id=temperature.city_id)

    resp = {
        "id": result.lastrowid,
        "date_time": temperature.date_time,
        "temperature": temperature.temperature,
        "city": city
    }

    return schemas.Temperature.model_validate(resp)


async def get_temperature_record_by_city_id(
        db: AsyncSession, city_id: int
) -> list[models.DBTemperature]:
    query = select(
        models.DBTemperature
    ).where(
        models.DBTemperature.city_id == city_id
    ).options(
        selectinload(
            models.DBTemperature.city
        )
    )
    temperature_list = await db.execute(query)

    return [temperature[0] for temperature in temperature_list.fetchall()]
