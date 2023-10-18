from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from city.models import DBCity


async def get_cities_list(db: AsyncSession) -> list[DBCity]:
    query = select(DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_single_city(city_id: int, db: AsyncSession) -> DBCity:
    query = select(DBCity).where(city_id == DBCity.id)
    result = await db.execute(query)
    city = result.scalar()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict:
    query = insert(DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_city(
        city_id: int,
        new_city: schemas.CityCreate,
        db: AsyncSession,
) -> DBCity:
    query = select(DBCity).where(city_id == DBCity.id)
    result = await db.execute(query)
    city = result.scalar()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city.name = new_city.name
    city.additional_info = new_city.additional_info

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(
        city_id: int,
        db: AsyncSession,
) -> dict:
    query = select(DBCity).where(city_id == DBCity.id)
    result = await db.execute(query)
    city = result.scalar()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()

    return {"message": "Deleted successfully"}
