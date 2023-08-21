from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from cities import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    """Get all cities from the database using SQLAlchemy querying."""
    cities = await db.execute(select(models.City))
    return cities.scalars().all() if cities else []


async def get_city_detail(
        db: AsyncSession,
        city_id: int
) -> models.City | None:
    """Get city by id."""
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar() if city else None


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
    """Get city by name."""
    query = select(models.City).where(models.City.name == name)
    city = await db.execute(query)
    return city.scalar() if city else None


async def create_city(
        db: AsyncSession,
        city_schema_data: schemas.CityCreate
) -> dict[str, str] | None:
    existing_city = await get_city_by_name(db, city_schema_data.name)
    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City with provided name already exists"
        )

    query = insert(models.City).values(
        name=city_schema_data.name,
        additional_info=city_schema_data.additional_info
    )

    result = await db.execute(query)
    await db.commit()

    response = {**city_schema_data.model_dump(), "id": result.lastrowid}
    return response


async def update_city(
        db: AsyncSession, city_id: int,
        city_schema_data: schemas.CityCreate
) -> models.City | None:
    """Update city."""
    existing_city = await get_city_by_name(db, city_schema_data.name)
    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City with provided name already exists"
        )
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(**city_schema_data.model_dump())
    )

    result = await db.execute(query)
    await db.commit()

    if result.rowcount:
        return await get_city_detail(db, city_id)

    return None


async def delete_city(db: AsyncSession, city_id: int) -> str:
    """Delete city."""
    query = delete(models.City).where(models.City.id == city_id)

    await db.execute(query)
    await db.commit()
    return "City deleted successfully"
