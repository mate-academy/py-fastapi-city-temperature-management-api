from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City
from app.city.schemas import CityCreateModel, CityModel


async def get_city_list(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(City))
    return list(result.all())


async def get_city_by_id(db: AsyncSession, id_: int) -> City | None:
    result = await db.scalars(select(City).where(City.id == id_))
    return result.one_or_none()


async def create_city(db: AsyncSession, data: CityCreateModel) -> City:
    stmt = insert(City).values(**data.model_dump()).returning(City)
    result = await db.execute(stmt)
    city = result.fetchone()[0]

    await db.commit()
    await db.refresh(city)

    return city


async def completely_update_city_by_id(
    db: AsyncSession,
    data: CityModel,
    id_: int
) -> City:
    stmt = update(City).where(City.id == id_).values(**data.model_dump())

    result = await db.execute(stmt)

    await db.commit()

    return result.fetchone()[0]


async def delete_city_by_id(
    db: AsyncSession,
    id_: int
) -> None:
    stmt = delete(City).where(City.id == id_)
    await db.execute(stmt)
