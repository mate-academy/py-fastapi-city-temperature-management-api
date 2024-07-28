from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import models
from src.city import schemas


def get_paginated(model: models.Base, offset: int, limit: int):
    return select(model).offset(offset).limit(limit)


async def get_cities(limit: int, offset: int, session: AsyncSession):
    stmt = get_paginated(models.City, offset, limit)

    cities_list = await session.execute(stmt)
    return [city[0] for city in cities_list.fetchall()]


async def retrieve_city(
    id: int,
    session: AsyncSession,
):
    stmt = select(models.City).filter(models.City.id == id)
    author = await session.execute(stmt)
    if not author.first():
        raise HTTPException(status_code=404, detail="City not found")
    return author.first()[0]


async def create_city(city: schemas.CityCreate, session: AsyncSession):
    stmt = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await session.execute(stmt)
    await session.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def update_city(
    id: int,
    city: schemas.CityBase,
    session: AsyncSession,
):
    stmt = update(models.City).where(models.City.id == id).values(**city)
    author = await session.execute(stmt)
    if not author.first():
        raise HTTPException(status_code=404, detail="City not found")
    return author.first()[0]


async def delete_city(
    id: int,
    session: AsyncSession,
):
    stmt = delete(models.City).where(models.City.id == id)
    author = await session.execute(stmt)
    if not author.first():
        raise HTTPException(status_code=404, detail="City not found")
    return author.first()[0]
