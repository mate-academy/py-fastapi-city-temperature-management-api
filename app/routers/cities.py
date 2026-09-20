from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from app import crud, models, schemas
from app.dependencies import DB

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def read_cities(db: DB):
    return await crud.get_all_cities(db)


@router.post(
    "/cities/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
async def create_cities(city: schemas.CityCreate, db: DB):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: DB):
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city_data: schemas.CityCreate, db: DB):
    result = await db.execute(
        select(models.CityDB).where(models.CityDB.id == city_id)
    )
    db_city = result.scalars().first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    for key, value in city_data.model_dump().items():
        setattr(db_city, key, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: DB):
    result = await db.execute(
        select(models.CityDB).where(models.CityDB.id == city_id)
    )
    db_city = result.scalars().first()

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    await db.delete(db_city)
    await db.commit()
    return None
