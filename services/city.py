from sqlite3 import IntegrityError

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import delete, insert, select, update

from dependecies.database import DataBaseDependency
from models.city import City
from schemes.city import CityCreate, CityUpdate


async def get_all_cities(db: DataBaseDependency):
    query = select(City)
    result = await db.execute(query)
    return result.scalars().all()


async def create_city(db: DataBaseDependency, city: CityCreate):
    data = city.model_dump()
    db_city = City(**data)
    try:
        query = insert(City).values(**data)
        await db.execute(query)
        await db.commit()
    except IntegrityError:
        await db.rollback()
    return db_city


async def change_city(db: DataBaseDependency, city_id: int, city: CityUpdate):
    data = city.model_dump(exclude_none=True)
    db_city = await db.get(City, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with {city_id} does not exist.",
        )
    try:
        query = update(City).where(City.id == city_id).values(**data)
        await db.execute(query)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City '{data['name']}' already exists.",
        )
    await db.refresh(db_city)
    return db_city


async def remove_city(db: DataBaseDependency, city_id: int):
    db_city = await db.get(City, city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with {city_id} does not exist.",
        )
    try:
        query = delete(City).where(City.id == city_id)
        await db.execute(query)
        await db.commit()
    except IntegrityError:
        await db.rollback()
    return db_city
