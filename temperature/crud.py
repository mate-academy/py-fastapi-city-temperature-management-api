from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ScalarResult, select, insert
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from temperature import models
from db.exc import DatabaseError


async def aget_temperatures_list(
    asession: AsyncSession, city_id: int | None = None
) -> ScalarResult[models.Temperature]:
    stmt = select(models.Temperature).options(
        joinedload(models.Temperature.city)
    )
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    return await asession.scalars(stmt)


async def acreate_temperatures(asession: AsyncSession, temp_list: list):
    stmt = insert(models.Temperature).values(temp_list)
    try:
        await asession.execute(stmt)
        await asession.commit()
    except IntegrityError as e:
        await asession.rollback()
        raise DatabaseError(e.orig)
