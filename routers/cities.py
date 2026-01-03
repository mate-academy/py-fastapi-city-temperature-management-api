from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate, City as CitySchema
from app.exceptions import not_found_error, bad_request_error

router = APIRouter(tags=["cities"])

@router.post("/", response_model=CitySchema, status_code=201)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new city.
    """
    try:
        db_city = City(name=city.name, additional_info=city.additional_info)
        db.add(db_city)
        await db.commit()
        await db.refresh(db_city)
        return db_city
    except Exception as e:
        await db.rollback()
        raise bad_request_error(f"Error creating city: {str(e)}")


@router.get("/", response_model=list[CitySchema])
async def get_cities(db: AsyncSession = Depends(get_db)):
    """
    Get all cities.
    """
    result = await db.execute(select(City))
    return result.scalars().all()


@router.get("/{city_id}", response_model=CitySchema)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get city by ID.
    """
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise not_found_error("City", city_id)
    return city


@router.put("/{city_id}", response_model=CitySchema)
async def update_city(city_id: int, city: CityUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update city by ID.
    """
    result = await db.execute(select(City).where(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if not db_city:
        raise not_found_error("City", city_id)

    try:
        if city.name is not None:
            db_city.name = city.name
        if city.additional_info is not None:
            db_city.additional_info = city.additional_info

        await db.commit()
        await db.refresh(db_city)
        return db_city
    except Exception as e:
        await db.rollback()
        raise bad_request_error(f"Error updating city: {str(e)}")


@router.delete("/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete city by ID.
    """
    result = await db.execute(select(City).where(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if not db_city:
        raise not_found_error("City", city_id)

    try:
        await db.delete(db_city)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise bad_request_error(f"Error deleting city: {str(e)}")
