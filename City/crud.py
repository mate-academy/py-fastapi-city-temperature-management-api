from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from City.models import DBCity
from City.schemas import CityCreate


async def get_all_city(db: AsyncSession) -> list[DBCity]:
    stmt = select(DBCity).options(selectinload(DBCity.temperatures))
    result = await db.scalars(stmt)

    return list(result.all())


async def get_city_by_id(
    db: AsyncSession,
    city_id: int
) -> DBCity | None:
    return await db.scalar(
        select(DBCity).where(DBCity.id == city_id)
    )


async def create_city(
    db: AsyncSession,
    city: CityCreate
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
    name: str
) -> DBCity | None:
    return await db.scalar(
        select(
            DBCity
        ).where(
            DBCity.name == name
        )
    )

async def delete_city(db: AsyncSession, city_id: int) -> DBCity | None:
    stmt = select(DBCity).options(selectinload(DBCity.temperatures)).where(DBCity.id == city_id)
    db_city = await db.scalar(stmt)

    if not db_city:
        return None

    await db.delete(db_city)
    await db.commit()

    return db_city
