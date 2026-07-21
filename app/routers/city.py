from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.city import crud, schemas, models
from app.dependencies import get_db

router = APIRouter()


@router.get("/cities", response_model=list[schemas.CityModel])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> list[models.City]:
    return await crud.get_city_list(db)


@router.get("/cities/{city_id}", response_model=schemas.CityModel)
async def get_single_city(
    city_id: int,
    db: AsyncSession = Depends(get_db)
) -> models.City:
    city = await crud.get_city_by_id(db, city_id)

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city


@router.post("/cities", response_model=schemas.CityModel)
async def write_city(
    data: schemas.CityCreateModel,
    db: AsyncSession = Depends(get_db)
) -> models.City:
    city = await crud.get_city_by_name(db, data.name)

    if city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )


    return await crud.create_city(db, data)


@router.put("/cities/{city_id}", response_model=schemas.CityModel)
async def modify_single_city(
    city_id: int,
    data: schemas.CityCreateModel,
    db: AsyncSession = Depends(get_db)
) -> models.City:
    city = await crud.get_city_by_id(db, city_id)
    stmt = select(models.City).where(models.City.name == data.name)
    result = await db.execute(stmt)

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    if result.scalar_one_or_none() and city.name != data.name:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )

    return await crud.completely_update_city_by_id(db, data, city_id)


@router.delete("/cities/{city_id}")
async def destroy_city(
    city_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    await crud.delete_city_by_id(db, city_id)
