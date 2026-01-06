from sqlalchemy.orm import selectinload
from city import schemas, models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_city_list(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10000,
) -> list[models.City]:
    stmt = await db.scalars(select(models.City).offset(skip).limit(limit))
    return list(stmt.all())


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
    stmt = await db.scalar(
        select(models.City)
        .where(models.City.name == name)
    )
    return stmt


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.get(models.City, city_id)


async def post_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def put_city(
        db: AsyncSession,
        city_id: int,
        city_data: schemas.CityCreate
) -> models.City | None:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return None
    db_city.name = city_data.name
    db_city.additional_info = city_data.additional_info
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def patch_city(
        db: AsyncSession,
        city_id: int,
        city_data: schemas.CityUpdate
) -> models.City | None:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return None
    if city_data.name is not None:
        db_city.name = city_data.name
    if city_data.additional_info is not None:
        db_city.additional_info = city_data.additional_info
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> bool:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return False
    await db.delete(db_city)
    await db.commit()
    return True


async def get_temperature_list(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
) -> list[models.Temperature]:
    stmt = await db.scalars(
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
        .offset(skip)
        .limit(limit))
    return list(stmt.all())


async def get_temperatures_for_city_by_id(
        db: AsyncSession,
        city_id: int,
        skip: int = 0,
        limit: int = 100,
) -> list[models.Temperature]:
    stmt = await db.scalars(
        select(models.Temperature)
        .where(models.Temperature.city_id == city_id)
        .options(selectinload(models.Temperature.city))
        .offset(skip)
        .limit(limit))
    return list(stmt.all())


async def create_temperature(
        db: AsyncSession,
        temp_list: list[models.Temperature],
):
    if not temp_list:
        return
    db.add_all(temp_list)
    await db.commit()
