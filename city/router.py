from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dependencies import get_db
from city import schemas, crud, models

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityResponse])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.CityResponse)
async def create_city(
        city: schemas.CityCreate,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_city(
        db=db,
        city=city
    )


@router.get("/cities/{city_id}/", response_model=schemas.CityResponse)
async def read_single_city(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.CityResponse)
async def update_city(
        city_id: int,
        city_data: schemas.CityUpdate,
        db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(models.City).where(models.City.id == city_id)
    )

    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    city.name = city_data.name
    city.additional_info = city_data.additional_info

    await db.commit()
    await db.refresh(city)

    return city


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(db_city)
    await db.commit()
