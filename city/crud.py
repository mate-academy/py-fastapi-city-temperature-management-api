from sqlalchemy import select
from dependencies import db_dependency
from database.models import City
from .schemas import CityCreate, CityUpdate
from .constraints import check_city_exists


async def city_create(db: db_dependency, city: CityCreate):
    create_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(create_city)
    await db.commit()
    return create_city


async def get_cities(db: db_dependency):
    query = select(City)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_by_id(db: db_dependency, city_id: int):
    city = await check_city_exists(db, city_id, city_name=None)
    return city


async def get_city_by_name(db: db_dependency, city_name: str):
    city = await check_city_exists(db, city_id=None, city_name=city_name)
    return city


async def update_city_info(db: db_dependency, update_info: CityUpdate, city_id: int):
    city = await check_city_exists(db, city_id, city_name=None)

    if update_info.name is not None:
        city.name = update_info.name
    if update_info.additional_info is not None:
        city.additional_info = update_info.additional_info

    await db.commit()
    db.refresh(city)

    return city


async def city_delete(db: db_dependency, city_id: int):
    city = await check_city_exists(db, city_id, city_name=None)
    await db.delete(city)
    await db.commit()
