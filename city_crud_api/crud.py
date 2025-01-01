from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city_crud_api import models, schemas


async def get_all_cities(db: AsyncSession):
    try:
        query = select(models.City)
        result = await db.execute(query)
        cities = result.scalars().all()
        if not cities:
            raise HTTPException(status_code=404, detail="No cities found in the database.")
        return cities
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch cities.")


async def get_city_by_id(db: AsyncSession, city_id: int):
    try:
        query = select(models.City).where(models.City.id == city_id)
        result = await db.execute(query)
        city = result.scalar_one_or_none()
        if not city:
            raise HTTPException(status_code=404, detail=f"City with ID {city_id} not found.")
        return city
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch the city.")


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    try:
        existing_city_query = select(models.City).where(models.City.name == city.name)
        existing_city_result = await db.execute(existing_city_query)
        existing_city = existing_city_result.scalar_one_or_none()
        if existing_city:
            raise HTTPException(status_code=400, detail=f"City with name '{city.name}' already exists.")

        query = (
            insert(models.City)
            .values(
                name=city.name,
                additional_info=city.additional_info,
            )
            .returning(models.City.id)
        )
        result = await db.execute(query)
        city_id = result.scalar_one()
        await db.commit()
        return {
            **city.dict(),
            "id": city_id
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create the city.")


async def update_city(db: AsyncSession, city: schemas.CityUpdate, city_id: int):
    try:
        city_in_db = await get_city_by_id(city_id=city_id, db=db)
        if not city_in_db:
            raise HTTPException(status_code=404, detail="City not found.")

        for key, value in city.dict(exclude_unset=True).items():
            setattr(city_in_db, key, value)

        await db.commit()
        await db.refresh(city_in_db)

        return city_in_db
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update the city.")


async def delete_city(db: AsyncSession, city_id: int):
    try:
        city = await get_city_by_id(db=db, city_id=city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found.")

        await db.delete(city)
        await db.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete the city.")
