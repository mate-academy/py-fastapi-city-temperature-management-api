from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, crud
from dependencies import get_session

router = APIRouter()


@router.get("/cities", response_model=list[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_session)):
    """Get all cities from database."""
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city_detail(
        city_id: int,
        db: AsyncSession = Depends(get_session)
):
    """Get city by id."""
    return await crud.get_city_detail(db=db, city_id=city_id)


@router.post("/cities", response_model=schemas.City)
async def create_city(
        city_schema_data: schemas.CityCreate,
        db: AsyncSession = Depends(get_session)
):
    """Create city."""
    return await crud.create_city(
        db=db,
        city_schema_data=city_schema_data
    )


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city_schema_data: schemas.CityCreate,
        db: AsyncSession = Depends(get_session)
):
    """Update city."""
    return await crud.update_city(
        db=db,
        city_id=city_id,
        city_schema_data=city_schema_data
    )


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_session)):
    """Delete city."""
    return await crud.delete_city(db=db, city_id=city_id)
