from fastapi import HTTPException

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_city_by_name(db: AsyncSession, name: str) -> models.City:
    query = select(models.City).where(models.City.name == name)
    city = await db.execute(query)
    return city.scalars().first()


async def post_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    if await get_city_by_name(db, city.name):
        raise HTTPException(
            status_code=400,
            detail=f"City {city.name} already exists"
        )
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return models.City(**resp)


async def get_city_list(db: AsyncSession) -> list[models.City]:
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_city_by_id(db: AsyncSession, id: int) -> models.City:
    query = select(models.City).where(models.City.id == id)
    city = await db.execute(query)
    city = city.scalars().first()
    if not city:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {id} not found"
        )
    return city


async def put_city(
        db: AsyncSession,
        id: int,
        city: schemas.CityUpdate
) -> models.City:
    db_city = await get_city_by_id(db=db, id=id)
    if city.name is not None:
        db_city.name = city.name
    if city.additional_info is not None:
        db_city.additional_info = city.additional_info
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, id: int) -> None:
    db_city = await get_city_by_id(db=db, id=id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
