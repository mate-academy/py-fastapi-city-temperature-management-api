from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload,  selectinload
from db.models import CityORM, TemperatureORM
from db.schemas import CityAddDTO
from tools.services import get_temperature


#==========================CITIES==============================
async def select_all_cities(db: AsyncSession) -> list[CityORM]:
    query = (
        select(CityORM)
        .options(selectinload(CityORM.temperatures))
    )
    cities = await db.execute(query)
    return cities.scalars().all()  # type: ignore


async def select_city_by_id(db: AsyncSession, city_id: int) -> CityORM | None:
    query = (
        select(CityORM)
        .where(CityORM.id == city_id)
        .options(selectinload(CityORM.temperatures))
    )
    result = await db.execute(query)
    city = result.scalars().first()
    return city # type: ignore


async def select_city_by_name(db: AsyncSession, name: str) -> CityORM | None:
    valid_name = name.lower().capitalize()
    query = (
        select(CityORM)
        .where(CityORM.name == valid_name)
        .options(selectinload(CityORM.temperatures))
    )
    result = await db.execute(query)
    return result.scalars().first() # type: ignore


async def create_city(db: AsyncSession, city_model: CityAddDTO) -> CityORM:
    valid_name = city_model.name.lower().capitalize()

    city_to_create = CityORM(
        name=valid_name,
        additional_info=city_model.additional_info
    )

    db.add(city_to_create)
    await db.commit()
    await db.refresh(city_to_create)
    return city_to_create


async def update_city(db: AsyncSession, city_to_update: CityORM, city_model: CityAddDTO) -> CityORM:
    city_dict = city_model.model_dump()

    for key, value in city_dict.items():
        if value:
            if key == "name":
                value = value.lower().capitalize()
            setattr(city_to_update, key, value)

    await db.commit()
    await db.refresh(city_to_update)
    return city_to_update


async def remove_city(db: AsyncSession, city_to_remove: CityORM) -> None:
    await db.delete(city_to_remove)
    await db.commit()
    return


#==========================Temperature==============================
async def fetch_and_store_all_temperatures(db: AsyncSession, cities: list[CityORM]):
    for city in cities:
        time_now = datetime.now().replace(microsecond=0)
        try:
            city_temp = await get_temperature(city_name=city.name)
        except KeyError:
            raise
        city_temperature = TemperatureORM(
            city_id=city.id,
            temperature=city_temp,
            date_time=time_now
        )
        db.add(city_temperature)

    await db.commit()
    return


async def select_temperature_by_city_id(db: AsyncSession, city_id):
    query = (
        select(TemperatureORM)
        .where(TemperatureORM.city_id == city_id)
        .options(joinedload(TemperatureORM.city))
    )
    result = await db.execute(query)
    return result.unique().scalars().all()


async def select_all_temperatures(db: AsyncSession) -> list[TemperatureORM]:
    query = (
        select(TemperatureORM)
        .options(joinedload(TemperatureORM.city))
    )
    result = await db.execute(query)
    return result.unique().scalars().all() # type: ignore
