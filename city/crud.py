from fastapi import (
    HTTPException,
    status
)

from sqlalchemy import (
    select,
    delete,
    update,
)

from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
)

from sqlalchemy.ext.asyncio import AsyncSession

from .models import City
from .schemas import CityCreateSchema


async def get_all_cities(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(City))
    return list(result.all())


async def create_city(
    db: AsyncSession,
    city_data: CityCreateSchema
) -> City:
    try:
        db_city = City(**city_data.model_dump())
        db.add(db_city)
        await db.commit()
        await db.refresh(db_city)
        return db_city
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City already exists"
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


async def delete_city_by_id(
    db: AsyncSession,
    city_id: int
) -> list[City]:
    try:
        db_city = await db.scalar(select(City).where(City.id == city_id))
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        await db.delete(db_city)
        await db.commit()
        cities = await db.scalars(select(City))
        return list(cities.all())
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


async def update_city_by_id(
    db: AsyncSession,
    city_id: int,
    city_data: CityCreateSchema,
) -> list[City]:
    try:
        db_city = await db.scalar(select(City).where(City.id == city_id))
        if not db_city:
            raise HTTPException(status_code=404, detail="City not found")
        await db.execute(
                update(City)
                .where(City.id == city_id)
                .values(**city_data.model_dump())
        )
        await db.commit()
        cities = await db.scalars(select(City))
        return list(cities.all())
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
