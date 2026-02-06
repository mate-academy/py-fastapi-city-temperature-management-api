from typing import Any, Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from city import schemas
from dependencies import paginate, get_db


async def get_all_cities(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: int = 1,
        size: int = 10,
        city: str | None = None,
) -> dict[str, Any]:
    query = select(DBCity)
    if city:
        query = query.where(
            DBCity.name.ilike(f"%{city}%")
        )
    return await paginate(db=db, query=query, page=page, size=size)


async def get_city_by_id(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int
) -> DBCity | None:
    db_city = select(DBCity).where(DBCity.id == city_id)
    return await db.scalar(db_city)


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> DBCity:
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city_by_name(
        db: AsyncSession,
        city_name: str
) -> DBCity | None:
    db_city = select(DBCity).where(DBCity.name == city_name)
    return await db.scalar(db_city)


async def delete_city_by_id(
        db: AsyncSession,
        city: DBCity
) -> dict:
    await db.delete(city)
    await db.commit()
    return {"Message": f"City {city.name} was deleted"}


async def city_update(
        db: AsyncSession,
        city: DBCity,
        update_data: dict
) -> DBCity | None:
    for key, value in update_data.items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city
