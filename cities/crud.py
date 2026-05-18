from sqlalchemy import select
from cities.models import City
from cities.schemas import CityCreate


async def get_city(db, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()
    return city

async def get_cities(db):
    result = await db.execute(select(City))
    cities = result.scalars().all()
    return cities

async def create_city(db, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def update_city(db, city_id: int, city: CityCreate):
    db_city = await get_city(db, city_id)
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def delete_city(db, city_id: int):
    city = await get_city(db, city_id)
    await db.delete(city)
    await db.commit()
    return city
