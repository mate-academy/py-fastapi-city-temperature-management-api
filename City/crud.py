from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession



from City import models, schemas


async def get_all_cities(
        db: AsyncSession
):
    stmt = select(models.City)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_city_by_id(
        db: AsyncSession,
        id: int
):

    stmt = select(models.City).where(models.City.id == id)
    result = await db.execute(stmt)

    city = result.scalars().first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city

async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
):
    stmt = select(models.City).where(models.City.name == city.name)
    result = await db.execute(stmt)
    existing = result.scalars().first()

    if existing:
        raise HTTPException(status_code=409, detail="City already exists")

    new_city = models.City(**city.model_dump())
    db.add(new_city)

    try:
        await db.commit()
    except IntegrityError:
        # Если уникальность нарушилась при конкурентной вставке — откатываем и возвращаем 409
        await db.rollback()
        raise HTTPException(status_code=409, detail="City already exists")

    await db.refresh(new_city)
    return new_city

async def update_city(
        db: AsyncSession,
        id: int,
        city: schemas.CityUpdate
):
    stmt = select(models.City).where(models.City.id == id)
    result = await db.execute(stmt)
    existing = result.scalars().first()

    if not existing:
        raise HTTPException(status_code=404, detail="City not found")

    city_data = city.model_dump(exclude_unset=True)
    for key, value in city_data.items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)
    return existing

async def delete_city(
        db: AsyncSession,
        id: int
):
    stmt = select(models.City).where(models.City.id == id)
    result = await db.execute(stmt)
    existing = result.scalars().first()

    if not existing:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(existing)
    await db.commit()
    return f"City with id {id} was deleted"
