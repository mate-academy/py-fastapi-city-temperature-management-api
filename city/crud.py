from sqlalchemy.orm import Session
from sqlalchemy import select

from city.city_models import City
from city import schemas


async def get_cities_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    result = await db.execute(select(City).offset(skip).limit(limit))
    return result.scalars().all()


async def get_city_by_id(db: Session, city_id: int):
    return await db.query(City).filter(City.id == city_id).first()


async def get_city_by_name(db: Session, city_name: str):
    return await db.query(City).filter(City.name == city_name).first()


async def create_city(db: Session, city_data: schemas.CityCreate):
    db_city = City(
        name=city_data.name,
        additional_info=city_data.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: Session, city_id: int, city_data: schemas.CityUpdate):
    db_city = await get_city_by_id(db, city_id)
    if db_city:
        db_city.name = city_data.name
        db_city.additional_info = city_data.additional_info
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: Session, city_id: int):
    db_city = await get_city_by_id(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city
