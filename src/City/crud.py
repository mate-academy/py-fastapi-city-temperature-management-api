from functools import wraps
from typing import List

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import insert, select, update, delete, desc
from sqlalchemy.orm import selectinload

from src.City.models import City
from src.Temperature.models import Temperature
from . import schemas


# I understand that it is desirable to do this in the router, but this decorator was created for development speed.
def commit_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db = kwargs.get("db") or next((arg for arg in args if isinstance(arg, AsyncSession)), None)
        if not db:
            raise ValueError("Session not found")

        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            await db.rollback()
            raise e
        else:
            await db.commit()
            return result

    return wrapper


@commit_decorator
async def create_new_city(db: AsyncSession, city: schemas.CityCreateOrUpdate) -> City:
    stmt = (
        insert(City)
        .values(**city.model_dump())
        .returning(City)
    )
    return (await db.execute(stmt)).scalar_one()


async def get_all_cities(db: AsyncSession) -> List[City]:
    return (
        await db.execute(select(City))
    ).scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    stmt = (
        select(City)
        .where(City.id == city_id)
        .options(selectinload(City.temperatures))
    )
    return (await db.execute(stmt)).scalar_one_or_none()


@commit_decorator
async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreateOrUpdate) -> City | None:
    subquery = (
        select(City.id)
        .where(
            City.id == city_id, City.name != city.name
        )
        .scalar_subquery()
    )
    await db.execute(
        delete(Temperature)
        .where(Temperature.city_id == subquery)
    )
    stmt = (
        update(City)
        .where(City.id == city_id)
        .values(**city.model_dump())
        .returning(City)
    )
    return (await db.execute(stmt)).scalar_one_or_none()


@commit_decorator
async def delete_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    stmt = (
        delete(City)
        .where(City.id == city_id)
        .returning(City)
    )
    return (await db.execute(stmt)).scalar_one_or_none()
