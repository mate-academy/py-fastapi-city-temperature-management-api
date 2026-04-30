from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, ScalarResult
from sqlalchemy.exc import IntegrityError, NoResultFound

from city import models, schemas
from db.exc import DatabaseError


async def aget_city(asession: AsyncSession, id: int) -> models.City | None:
    stmt = select(models.City).where(models.City.id == id)
    return await asession.scalar(stmt)


async def aget_cities_list(
    asession: AsyncSession
) -> ScalarResult[models.City]:
    stmt = select(models.City)
    return await asession.scalars(stmt)


async def acreate_city(
    asession: AsyncSession, city: schemas.CityCreate
) -> models.City:
    db_city = models.City(**city.model_dump())
    try:
        asession.add(db_city)
        await asession.commit()
        await asession.refresh(db_city)
    except IntegrityError as e:
        await asession.rollback()
        raise DatabaseError(e.orig)
    return db_city


async def aupdate_city(
    asession: AsyncSession, city_id: int, city: schemas.CityEdit,
) -> models.City:
    stmt = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(**city.model_dump(exclude_unset=True))
        .returning(models.City)
    )
    try:
        result = await asession.execute(stmt)
        updated_city = result.scalar_one()
        await asession.commit()
        await asession.refresh(updated_city)
        return updated_city
    except (IntegrityError, NoResultFound) as e:
        await asession.rollback()
        if hasattr(e, "orig"):
            raise DatabaseError(e.orig)
        raise DatabaseError


async def adelete_city(
        asession: AsyncSession, city_id: int
) -> None:
    async with asession.begin():
        city = await asession.get(models.City, city_id)
        if not city:
            raise DatabaseError(message={"city_id": "Invalid value"})
        await asession.delete(city)
